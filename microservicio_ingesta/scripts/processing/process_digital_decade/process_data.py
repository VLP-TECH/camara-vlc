from modelos.models import Processor_digital_decade as Processor
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

DATOS = [
    Processor(
        indicador = CATALOGO_COMPLETO['Cobertura de redes de muy alta capacidad (VHCN)'],
        nombre_archivo='cobertura_de_redes_vhcn',
        nombre_resultado='%(hogares)',
        procesado=True,
    ),
    Processor(
        indicador = CATALOGO_COMPLETO['Empresas que utilizan software de gestión de relaciones con los clientes (CRM)'],
        nombre_archivo='empresas_usan_crm',
        nombre_resultado='%(empresas)',
        procesado=True
    )
]

def processor_digital_decade():
    lista_resultados = []
    for indicador in DATOS:
        lista_resultados.append(indicador.procesar())

    return lista_resultados