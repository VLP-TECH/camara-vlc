from modelos.models import Colletor_cnmc as Collector
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

URL_TELECO = 'https://catalogodatos.cnmc.es/api/3/action/datastore_search?limit=32000&resource_id=1efe6d64-72a8-4f45-a36c-691054f3e277'
URL_INGRESOS = 'https://catalogodatos.cnmc.es/api/3/action/datastore_search?limit=32000&resource_id=5e2d8f37-2385-4774-82ec-365cd83d65bd'

FUENTES = [
        Collector(
            indicador = CATALOGO_COMPLETO['Adopción de banda ancha móvil (suscripciones/100 personas)'],
            url = URL_TELECO,
            nombre_archivo = 'telecomunicaciones.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Precio relativo de banda ancha'],
            url = URL_INGRESOS,
            nombre_archivo = 'ingresos.json'
        )
    ]

def collector_cnmc():
    for indicador in FUENTES:
        indicador.recoger()
