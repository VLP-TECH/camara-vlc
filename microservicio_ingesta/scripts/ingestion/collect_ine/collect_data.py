from modelos.models import Collector_ine as Collector
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

FUENTES = [
        Collector(
            id='56945',
            nombre_archivo='poblacion_por_provincia.px',
            tipo_tabla='t'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Teletrabajo'],
            id = '49858',
            nombre_archivo = 'empresas_permiten_teletrabajo.px',
            tipo_tabla = 'tpx'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Empresas con infraestructura en la nube'],
            id = '59890',
            nombre_archivo = 'empresas_servicios_cloud_computing.px',
            tipo_tabla = 'tpx'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Número de empresas que realizan I+D en el sector TIC'],
            id = '67905',
            nombre_archivo = 'empresas_tic_actividades_i+d.px',
            tipo_tabla = 'tpx'
        )
    ]

def collector_ine():
    for indicador in FUENTES:
        indicador.recoger()