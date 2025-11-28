from modelos.models import Processor_macro as Processor
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

def processor_rnpc():
    rnpc = Processor(
        indicador=CATALOGO_COMPLETO['Precio relativo de banda ancha'],
        descripcion_dato='Renta nacional bruta per cápita',
        nombre_archivo='rnbpc',
        nombre_resultado='Euros',
        nombre_antiguo='RNB per Cápita (€)'
    )
    datos_guia = rnpc.procesar() 

    return datos_guia
