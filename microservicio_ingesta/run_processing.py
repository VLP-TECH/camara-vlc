from microservicio_ingesta.scripts.processing.process_eurostat.process_data import processor_eurostat
from microservicio_ingesta.scripts.processing.process_ine.process_data import processor_ine
from microservicio_ingesta.scripts.processing.process_cnmc.process_data import processor_cnmc
from microservicio_ingesta.scripts.processing.process_digital_decade.process_data import processor_digital_decade
from microservicio_ingesta.scripts.processing.process_base.process_rnpc import processor_rnpc
from modelos.escribir_ficheros import FileWriter
import asyncio

OUTPUT_RESULTADO = 'database/guia_datos.py'
NOMBRE_VARIABLE = 'GUIA_DATOS_PROCESADOS'

def process_processor():
    lista_resultados = []
    print('[1/5] -- Procesando datos de eurostat...')
    lista_resultados.extend(processor_eurostat())

    print('[2/5] -- Procesando datos de ine...')
    lista_resultados.extend(processor_ine())

    print('[3/5] -- Procesando datos de cnmc...')
    lista_resultados.extend(processor_cnmc())

    print('[4/5] -- Procesando datos de digital-decade')
    lista_resultados.extend(processor_digital_decade())

    print('[5/5] -- Procesando algunos datos extra...')
    lista_resultados.append(processor_rnpc())

    return lista_resultados


async def escribir(detalles, escritor):
    async with escritor as fw:
        for detalle in detalles:
            await fw.agregar_elemento(detalle)


def processing():
    detalles_datos = process_processor()

    escritor = FileWriter(
        output=OUTPUT_RESULTADO,
        nombre_variable=NOMBRE_VARIABLE
    )

    asyncio.run(escribir(detalles_datos, escritor))

if __name__ == '__main__':
    processing()