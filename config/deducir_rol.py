from data.processed.indicadores.indicators import CATALOGO_COMPLETO
from data.processed.indicadores.formulas import CATALOGO_OPERACIONES
import asyncio
from ollama_scripts.ecosystem_model import ChatModel
import json
from modelos.escribir_ficheros import FileWriter


RUTA_SALIDA = 'data/processed/indicadores/roles.py'
CONTENIDO_INICIO = """# -*- coding: utf-8 -*-
# ¡ATENCIÓN! ESTE ARCHIVO ES GENERADO AUTOMÁTICAMENTE.
# NO LO EDites A MANO. EJECUTA ESTE SCRIPT PARA ACTUALIZARLO.

# Este catálogo contiene la clasificación de operaciones para cada indicador,
# generada a partir de un LLM.

CATALOGO_ROLES = [
    """


SYSTEM_PROMPT_ROLES = """
Eres un analista de datos experto. Tu tarea es asignar un rol funcional a cada componente de datos de un indicador, basándote en la fórmula de cálculo y el tipo de operación.

## 1. Roles Válidos
Debes asignar a cada componente de datos UNO de los siguientes roles:
- NUMERADOR: La parte superior de una fracción (en un RATIO).
- DENOMINADOR: La parte inferior de una fracción.
- VALOR_A_ESCALAR: El valor principal que se está normalizando.
- MINIMO_ESCALA: El valor mínimo de referencia para una escala.
- MAXIMO_ESCALA: El valor máximo de referencia para una escala.
- INDICE_A_PROMEDIAR: Un valor que forma parte de un índice compuesto.

## 2. Formato de Salida Obligatorio
Tu respuesta debe ser ÚNICAMENTE un JSON válido con la siguiente estructura. No incluyas texto adicional.
La estructura es: {"resultado": OK, "respuesta": <[{"nombre_indicador": "<Nombre_del_indicador>", "componentes": [{"descripcion_dato": "<descripcion_dato>", "rol": "<TIPO_DE_ROL_ELEGIDO>"}]}]>}

## 3. Ejemplos Concretos

### Ejemplo 1
Entrada:
- Nombre: Densidad de startups
- Operación: RATIO
- Fórmula: Número de startups tecnológicas por cada 1.000 empresas activas en la región
- Datos: ['Nº de startups tecnológicas', 'Nº de empresas activas en la región']

Salida JSON:
{"nombre_indicador": "Densidad de startups", "componentes": [{"descripcion_dato": "Nº de startups tecnológicas", "rol": "NUMERADOR"}, {"descripcion_dato": "Nº de empresas activas en la región", "rol": "DENOMINADOR"}]}

### Ejemplo 2
Entrada:
-Nombre: Productividad en empresas digitalizadas
-Operación: VALOR_ESCALADO
-Fórmula: Valor añadido bruto por empleado en empresas con alto nivel de digitalización
-Datos: ['VAB total de empresas digitalizadas', 'Nº total de empleados en empresas digitalizadas']

Salida JSON:
{"nombre_indicador": "Productividad en empresas digitalizadas", "componentes": [{"descripcion_dato": "VAB total de empresas digitalizadas", "rol": "VALOR_A_ESCALAR"}, {"descripcion_dato": "Nº total de empleados en empresas digitalizadas", "rol": "DENOMINADOR"}]}
"""

def fusionar_datos():
    operaciones_map = {item['nombre']: item['operacion'] for item in CATALOGO_OPERACIONES}

    datos_fusionados = []
    for nombre, indicador_obj in CATALOGO_COMPLETO.items():
        # Busca la operación en el mapa. Si no la encuentra, usa un valor por defecto.
        operacion = operaciones_map.get(nombre, 'AGREGACION_DIRECTA')

        # Crea un diccionario con todos los datos necesarios para tu tabla
        datos_completos = {
            'nombre': indicador_obj.nombre,
            'formula': operacion,
            'datos': indicador_obj.datos
        }

        datos_fusionados.append(datos_completos)

    return datos_fusionados

async def extraer_rol(datos_llm):
    user_prompt = f'''
    Ahora, procesa la siguiente lista de indicadores y genera el array JSON correspondiente como se te ha instruido.

    ### Indicadores a Procesar:
    {datos_llm}
    '''
    print('enviando solicitud a ollama')
    response = await instancia.async_chat(
        model='qwen3:1.7b',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT_ROLES},
            {'role': 'user', 'content': user_prompt}
        ],
        format='json'
    )

    return response['message']['content']

async def formatear_agregacion(lista:list):
    {"nombre_indicador": "Volumen de inversión privada en startups tecnológicas", "componentes": [{"nombre_dato": "Volumen de inversión privada en startups tecnológicas", "rol": "VALOR_A_AGREGAR"}]}
    lista_formateada = []
    for dato in lista:
        lista_formateada.append({
            'nombre_indicador': dato['nombre'],
            'componentes': [{
                'descripcion_dato': dato['datos'][0],
                'rol': 'VALOR_A_AGREGAR'
                }]
        })

    return lista_formateada

async def formatear_porcentajes(lista: list):
    lista_formateada = []
    for indicador in lista:
        asignaciones = []
        for i, dato in enumerate(indicador['datos']):
            if i % 2 == 0:
                asignaciones.append('NUMERADOR')
            else:
                asignaciones.append('DENOMINADOR')

        lista_formateada.append({
        'nombre_indicador': indicador['nombre'],
        'componentes': [
            {
                'descripcion_dato': descripcion,
                'rol': dato
            } 
            for dato, descripcion in zip(asignaciones, indicador['datos'])
            ]
        })
    
    return lista_formateada

async def limpiar_agregacion(datos: list):

    lista_agregaciones = [indicador for indicador in datos if indicador['formula'] == 'AGREGACION_DIRECTA']
    agregaciones_content = await formatear_agregacion(lista_agregaciones)

    nombres_filtrados_agregaciones = {item['nombre'] for item in lista_agregaciones}
    lista_sin_agregaciones = [indicador for indicador in datos if indicador['nombre'] not in nombres_filtrados_agregaciones]

    lista_porcentajes = [
        indicador for indicador in lista_sin_agregaciones if indicador['formula'] == 'PORCENTAJE'
    ]

    porcentajes_content = await formatear_porcentajes(lista_porcentajes)

    agregaciones_content.extend(porcentajes_content)

    nombres_filtrados_porcentajes = [item['nombre'] for item in lista_porcentajes]
    lista_sin_porcentajes = [indicador for indicador in lista_sin_agregaciones if indicador['nombre'] not in nombres_filtrados_porcentajes]

    return lista_sin_porcentajes, agregaciones_content

async def procesar(datos_fusionados):
    
    lista_limpia, content = await limpiar_agregacion(datos_fusionados)

    datos_para_llm = [
        f"Nombre: {indicador['nombre']}\nFórmula: {indicador['formula']}\nDatos: {indicador['datos']}"
        for indicador in lista_limpia
    ]

    tamano_lote = 10
    lista_roles = []

    for i in range(0, len(datos_para_llm), tamano_lote):
        # Obtiene el lote actual usando slicing.
        lote = datos_para_llm[i:i + tamano_lote]

        json_string =  await extraer_rol(lote)

        json_formato = json.loads(json_string)
        print (json_formato)
        lista_roles.extend(json_formato['respuesta'])

    lista_roles.extend(content)

    async with escritor as fw:
        for rol in lista_roles:
            await fw.agregar_elemento(rol)


if __name__ == '__main__':
    escritor = FileWriter(
        output=RUTA_SALIDA,
        nombre_variable='CATALOGO_ROLES'
    )

    instancia = ChatModel('qwen3:1.7b')
    datos_fusionados = fusionar_datos()
    asyncio.run(procesar(datos_fusionados))