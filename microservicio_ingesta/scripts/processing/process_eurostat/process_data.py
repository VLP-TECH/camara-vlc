from modelos.models import Processor_eurostat as Processor
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

DATOS = [
        Processor(
            nombre_archivo = 'poblacion_por_pais',
            nombre_resultado = 'poblacion',
            descripcion_dato='Población total'
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Empresas que usan inteligencia artificial'],
            nombre_archivo = 'empresas_uso_ia',
            nombre_resultado = '%(empresas)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Empresas que analizan big data de cualquier fuente de datos'],
            nombre_archivo = 'empresas_big_data',
            nombre_resultado = '%(empresas)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Empresas que comparten información electrónica internamente con un ERP'],
            nombre_archivo = 'empresas_erp_procesos_internos',
            nombre_resultado = '%(empresas)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Empresas que tienen un sitio web o página de inicio'],
            nombre_archivo = 'empresas_presencia_web_propia',
            nombre_resultado = '%(empresas)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Empresas que utilizan el mercado de comercio electrónico para ventas'],
            nombre_archivo = 'empresas_venta_online',
            nombre_resultado = '%(empresas)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Personas con habilidades digitales básicas'],
            nombre_archivo = 'habilidades_digitales_basicas',
            nombre_resultado = '%(16-74 annos)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Personas con habilidades digitales generales superiores a las básicas'],
            nombre_archivo = 'habilidades_digitales_superior_a_basica',
            nombre_resultado = '%(16-74 annos)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Personas que interactúan en línea con las autoridades públicas'],
            nombre_archivo = 'interaccion_autoridades_publicas',
            nombre_resultado = '%(16-74 annos)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Usuarios que usan banca online'],
            nombre_archivo = 'personas_servicio_banca_electronica',
            nombre_resultado = '%(16-74 annos)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Uso regular de Internet'],
            nombre_archivo = 'personas_uso_internet_una_vez_semana',
            nombre_resultado = '%(16-74 annos)',
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Empresas que utilizan las redes sociales'],
            nombre_archivo = 'empresas_uso_redes_sociales',
            nombre_resultado = '%(empresas)',
            procesado = True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Formación en TIC en empresas'],
            nombre_archivo = 'empresas_formacion_empleados_tic',
            nombre_resultado = '%(empresas)',
            procesado=True
        )
    ]

def processor_eurostat():

    poblacion_por_pais_y_edad = Processor(
            nombre_archivo = 'poblacion_por_pais_y_edad',
            nombre_resultado = 'poblacion',
            descripcion_dato='Población total entre 16 y 74 años'
        )
    

    lista_resultados = []
    lista_resultados.append(poblacion_por_pais_y_edad.depurar_datos_franjas_edad())
    
    for indicador in DATOS:
        lista_resultados.append(indicador.processar())

    return lista_resultados