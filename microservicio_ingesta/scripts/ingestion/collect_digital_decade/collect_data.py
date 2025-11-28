from modelos.models import Collector_digital_decade as Collector
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

FUENTES = [
    Collector(
        indicador = CATALOGO_COMPLETO['Cobertura de redes de muy alta capacidad (VHCN)'],
        url='https://digital-decade-desi.digital-strategy.ec.europa.eu/datasets/key-indicators/charts/analyse-one-indicator-and-compare-countries?indicator=bb_vhcncov&indicatorGroup=broadband&breakdown=total_pophh&unit=pc_hh&country=AT,BE,BG,HR,CY,CZ,DK,EE,EU,FI,FR,DE,EL,HU,IS,IE,IT,LV,LT,LU,MT,NL,NO,PL,PT,RO,SK,SI,ES,SE,UK',
        nombre_archivo='cobertura_de_redes_vhcn'
    ),
    Collector(
        indicador = CATALOGO_COMPLETO['Empresas que utilizan software de gestión de relaciones con los clientes (CRM)'],
        url = 'https://digital-decade-desi.digital-strategy.ec.europa.eu/datasets/key-indicators/charts/analyse-one-indicator-and-compare-countries?indicator=e_crman&indicatorGroup=ebusiness&unit=pc_ent&country=AT,BE,BG,HR,CY,CZ,DK,EE,EU,FI,FR,DE,EL,HU,IE,IT,LV,LT,LU,MT,NL,PL,PT,RO,SK,SI,ES,SE',
        empresa = True,
        nombre_archivo='empresas_usan_crm'
    )
]

def collector_digital_decade():
    for indicador in FUENTES:
        indicador.recoger()