import datetime
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
from pathlib import Path
import json

# Lista de códigos de sector NACE para iterar
LISTA_BREAKDOWNS_EMPRESA = [
'c', 'e', 'f', 'g', 'h', 'i', 'ict', 'j', 'l68', 'm', 'n'
]

async def get_dynamic_html(url: str) -> str | None:
    """
    Navega a una URL usando Playwright y espera a que el contenido dinámico (el gráfico) cargue.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"Navegando a: {url}")
        try:
            # Navegar a la URL. 'domcontentloaded' es suficiente porque vamos a añadir una espera manual.
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)

            # --- LA CLAVE DEL ARREGLO ESTÁ AQUÍ ---
            # Esperamos explícitamente a que el selector del gráfico aparezca.
            # Este selector apunta a las barras de datos del gráfico. Si aparecen, sabemos
            # que el JavaScript ha terminado de renderizar la visualización.
            # Si no aparece en 30 segundos (timeout), lanzará una excepción.
            await page.wait_for_selector('g.highcharts-series-group path', timeout=30000)
            
            print("Contenido dinámico cargado con éxito.")
            content = await page.content()

        except PlaywrightTimeoutError:
            # Si el selector del gráfico no aparece en el tiempo especificado,
            # significa que probablemente no hay datos para esta combinación.
            print(f"AVISO: No se encontró el gráfico en la página para la URL. Es posible que no haya datos.")
            content = None # Devolvemos None para indicar que no se encontró contenido.
        
        except Exception as e:
            print(f"Ocurrió un error inesperado con Playwright: {e}")
            content = None

        finally:
            await browser.close()
        
        return content

async def comprobar_respuesta_nace(content: str, cod_nace: str) -> str:
    """
    Parsea el contenido HTML para extraer los datos del gráfico y los devuelve en un DataFrame.
    Si no hay datos, devuelve un DataFrame vacío.
    """
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')

    # Verificamos qué filtro está seleccionado. Si es "All enterprises", significa que
    # la página no cargó el desglose para el 'cod_nace' específico y no debemos scrapear.
    try:
        breakdown_label = soup.find('label', attrs={'for': 'breakdown'})
        if breakdown_label:
            parent_div = breakdown_label.find_parent('div', class_='chart-filter')
            selected_filter_span = parent_div.select_one('div.multiselect__tags span')
            
            # Si el filtro muestra "All enterprises" y no estamos pidiendo explícitamente los datos generales...
            if selected_filter_span and selected_filter_span.text.strip() == 'All enterprises' and cod_nace != 'general':
                print(f"AVISO: La página para el sector '{cod_nace}' muestra 'All enterprises'. Omitiendo datos.")
                return None
            else:
                return content
    except Exception as e:
        print(f"No se pudo comprobar el filtro de desglose, continuando con el scraping. Error: {e}")


async def obtener_anno_display(content):
    soup = BeautifulSoup(content, 'html.parser')

    period_label = soup.find('label', attrs={'for': 'period'})
    if period_label:
        parent_div = period_label.find_parent('div', class_='chart-filter')
        selected_filter_span = parent_div.select_one('div.multiselect__tags span')
        
        return int(selected_filter_span.text.strip())
    
async def validar_valores_nulos(content):
    soup = BeautifulSoup(content, 'html.parser')
    grafico_paths = soup.select('g.highcharts-tracker path[aria-label]')

    if not grafico_paths:
        return False
    
    datos_extraidos = [i.get('aria-label') for i in grafico_paths]

    for item in datos_extraidos:
        if ',' in item:
            partes = item.split(',', 1)
            # Limpiamos el nombre del país y el valor (quitando el punto y el %)
            valor_str = partes[1].strip().rstrip('.%')
            if valor_str != '0':
                return True
            
    return False


async def validar_cods_nace(url):
    cods_nace_validos = []
    for cod_nace in LISTA_BREAKDOWNS_EMPRESA:
        content = await get_dynamic_html(f'{url}&breakdown=nace_{cod_nace}')
        if  await comprobar_respuesta_nace(content, cod_nace):
            cods_nace_validos.append(cod_nace)

    return cods_nace_validos


async def crear_dataframe_por_sectores(url_base: str, empresa: bool, output_path: str):
    """
    Orquesta el proceso de scraping para uno o varios sectores y guarda el resultado.
    """
    content_inicial = await get_dynamic_html(url_base)
    act_year = int(await obtener_anno_display(content_inicial))
    obj_year = act_year - 10
    json_contents = {}

    if empresa:
        lista_breakdowns_local = await validar_cods_nace(url_base)
    
    # Iteramos sobre cada código de sector para las empresas
    for year in range(act_year, obj_year, -1):
        if year not in json_contents:
            json_contents[year] = {}

        url_year = f'{url_base}&period={year}'

        if empresa:
            for cod_nace in lista_breakdowns_local:
                url_sector = f'{url_year}&breakdown=nace_{cod_nace}'
                contenido_html = await get_dynamic_html(url_sector)
                content_sector = await comprobar_respuesta_nace(contenido_html, cod_nace)

                if content_sector and (year != await(obtener_anno_display(content_sector)) or not await validar_valores_nulos(content_sector)):
                    break

                if content_sector:
                    json_contents[year][cod_nace] = content_sector

        else:
            # Caso para cuando no se filtra por empresa/sector
            contenido_html = await get_dynamic_html(url_year)
            json_contents[year]['general'] = contenido_html
        
    if json_contents:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_contents, f, ensure_ascii=False, indent=4)


def recoger_digital(empresa: bool, url: str, output_dir: Path, nombre_archivo: str):
    """
    Función principal que inicia el proceso de scraping.
    """
    # Asegurarse de que el directorio de salida exista
    # output_dir.mkdir(parents=True, exist_ok=True)
    ruta_completa_destino = output_dir / nombre_archivo

    asyncio.run(crear_dataframe_por_sectores(url, empresa, ruta_completa_destino))


