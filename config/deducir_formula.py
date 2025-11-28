import ollama
from data.processed.indicadores.indicators import CATALOGO_COMPLETO
import json
from ollama_scripts.ecosystem_model import ChatModel
import asyncio
from modelos.escribir_ficheros import FileWriter

RUTA_SALIDA = 'data/processed/indicadores/formulas.py'
NOMBRE_VARIABLE = 'CATALOGO_OPERACIONES'

async def extraer_formula(lista_indicadores: list) -> list:

# - AGREGACION_DIRECTA: Para sumas o conteos totales. Busca palabras clave como *Nº*, "Suma total", "Número de", "Conteo total", "Recuento". Debe tener *SOLO* 1 dato
#     - PORCENTAJE: Para fórmulas que calculan explícitamente un porcentaje (%). Busca el símbolo *"%"* o la palabra "tasa".
    # - TASA_CRECIMIENTO: Para medir el cambio de un valor a lo largo del tiempo.
    #     - PORCENTAJE: Para fórmulas que calculan explícitamente un porcentaje (%). Busca en la fórmula de calculo el contenido (dato / dato) x 100".

    system_prompt = '''
    Eres un analista de datos experto. Tu tarea es clasificar indicadores según su fórmula de cálculo, los datos que requiera y generar un array JSON.

    ## 1. Tipos de Operación Válidos y sus Definiciones
    Debes usar EXCLUSIVAMENTE uno de los siguientes tipos:
    

    - RATIO: Para la comparación entre dos números que NO es un porcentaje. Busca "por cada", "relación entre".
    - VALOR_ESCALADO: Para valores que han sido normalizados o ajustados a una escala. Busca "escalado", "escala".
    - INDICE_COMPUESTO: Para fórmulas complejas que combinan múltiples factores o no encajan en las anteriores. Ej: "Composición compleja".

    ## 2. Formato de Salida Obligatorio
    Tu respuesta debe ser ÚNICAMENTE un JSON válido, con una lista de JSON para cada uno de los indicadores. No incluyas texto adicional antes o después del JSON.
    La estructura es: {"resultado": OK, "respuesta": <{"nombre": "<nombre_del_indicador>", "operacion": "<TIPO_DE_OPERACION_ELEGIDO>"}>}

    ## 3. Ejemplos Concretos
    ### Ejemplo 1
    Entrada:
    Nombre: Volumen de inversión privada en startups tecnológicas
    Fórmula: Suma total (en €) de la inversión privada anual en startups tecnológicas registradas en la región

    Salida JSON:
    [{"nombre": "Volumen de inversión privada en startups tecnológicas", "operacion": "AGREGACION_DIRECTA"}]

    ### Ejemplo 2
    Entrada:
    Nombre: Densidad de startups
    Fórmula: Número de startups tecnológicas por cada 1.000 empresas activas en la región

    Salida JSON:
    [{"nombre": "Densidad de startups", "operacion": "RATIO"}]

    ### Ejemplo 3
    Entrada:
    Nombre: Inversión pública en TIC por habitante (gasto tecnológico del sector público)
    Fórmula: Total anual de gasto TIC del sector público regional / Población total

    Salida JSON:
    [{"nombre": "Disponibilidad de servicios públicos digitales", "operacion": "RATIO"}]

    /nothink
    '''

    user_prompt = f'''
    Ahora, procesa la siguiente lista de indicadores y genera el array JSON correspondiente como se te ha instruido.

    ### Indicadores a Procesar:
    {lista_indicadores}
    '''
    print('enviando solicitud a ollama')
    response = await instancia.async_chat(
        model='qwen3:1.7b',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        format='json'
    )

    return response['message']['content']


async def filtro_inicial():
    lista_indicadores = CATALOGO_COMPLETO.copy()

    lista_agregaciones = [
        {'nombre': indicador.nombre, 'operacion': 'AGREGACION_DIRECTA'} 
        for indicador in lista_indicadores.values() 
        if len(indicador.datos) == 1 and indicador.datos[0] != 'nan'
        ]
    
    nombres_filtrados_agregaciones = {item['nombre'] for item in lista_agregaciones}
    lista_sin_agregaciones = [indicador for indicador in CATALOGO_COMPLETO.values() if indicador.nombre not in nombres_filtrados_agregaciones]
    
    lista_porcentajes = [
        {'nombre': indicador.nombre, 'operacion': 'PORCENTAJE'} 
        for indicador in lista_sin_agregaciones 
        if '%' in indicador.formula_calculo or '× 100' in indicador.formula_calculo
        ]
    
    nombres_filtrados_porcentajes = {item['nombre'] for item in lista_porcentajes}
    nueva_lista = [indicador for indicador in CATALOGO_COMPLETO.values() if indicador.nombre not in nombres_filtrados_porcentajes and indicador.nombre not in nombres_filtrados_agregaciones]

    lista_porcentajes.extend(lista_agregaciones)

    print(lista_porcentajes)
    return nueva_lista, lista_porcentajes


async def iterar_modelo():

    lista_indicadores, content = await filtro_inicial()

    datos_para_llm = [
        f"Nombre: {indicador.nombre}\nFórmula: {indicador.formula_calculo}\nDatos: {indicador.datos}"
        for indicador in lista_indicadores
    ]

    tamano_lote = 10
    lista_formulas = []

    for i in range(0, len(datos_para_llm), tamano_lote):
        # Obtiene el lote actual usando slicing.
        lote = datos_para_llm[i:i + tamano_lote]

        json_string =  await extraer_formula(lote)
        json_formato = json.loads(json_string)

        lista_formulas.extend(json_formato['respuesta'])

    lista_formulas.extend(content)

    async with escritor as fw:
        for formula in lista_formulas:
            await fw.agregar_elemento(formula)


if __name__ == '__main__':

    escritor = FileWriter(
        output=RUTA_SALIDA,
        nombre_variable=NOMBRE_VARIABLE
    )
    
    instancia = ChatModel('qwen3:1.7b')
    asyncio.run(iterar_modelo())

