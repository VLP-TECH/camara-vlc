from modelos.models import Collector_eurostat as Collector
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

FUENTES = [
        Collector(
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjan?format=JSON&age=Y14&age=Y15&age=Y16&age=Y17&age=Y18&age=Y19&age=Y20&age=Y21&age=Y22&age=Y23&age=Y24&age=Y25&age=Y26&age=Y27&age=Y28&age=Y29&age=Y30&age=Y31&age=Y32&age=Y33&age=Y34&age=Y35&age=Y36&age=Y37&age=Y38&age=Y39&age=Y40&age=Y41&age=Y42&age=Y43&age=Y44&age=Y45&age=Y46&age=Y47&age=Y48&age=Y49&age=Y50&age=Y51&age=Y52&age=Y53&age=Y54&age=Y55&age=Y56&age=Y57&age=Y58&age=Y59&age=Y60&age=Y61&age=Y62&age=Y63&age=Y64&age=Y65&age=Y66&age=Y67&age=Y68&age=Y69&age=Y70&age=Y71&age=Y72&age=Y73&age=Y74&sex=T&lang=EN',
            nombre_archivo = 'poblacion_por_pais_y_edad.json'
        ),
        Collector(
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tps00001?format=JSON&indic_de=JAN&lang=EN',
            nombre_archivo = 'poblacion_por_pais.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Empresas que usan inteligencia artificial'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ain2?format=JSON&unit=PC_ENT&size_emp=GE10&nace_r2=C&nace_r2=E&nace_r2=F&nace_r2=G&nace_r2=H&nace_r2=I&nace_r2=ICT&nace_r2=J&nace_r2=M&nace_r2=N&nace_r2=L68&indic_is=E_AI_P1ANY&lang=EN',
            nombre_archivo = 'empresas_uso_ia.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Empresas que analizan big data de cualquier fuente de datos'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_bdn2?format=JSON&unit=PC_ENT&size_emp=GE10&nace_r2=C&nace_r2=F&nace_r2=G&nace_r2=H&nace_r2=I&nace_r2=ICT&nace_r2=J&nace_r2=L68&nace_r2=N&indic_is=E_BDA&lang=EN',
            nombre_archivo = 'empresas_big_data.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Empresas que comparten información electrónica internamente con un ERP'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_iipn2?format=JSON&unit=PC_ENT&size_emp=GE10&nace_r2=C&nace_r2=E&nace_r2=F&nace_r2=G&nace_r2=H&nace_r2=I&nace_r2=ICT&nace_r2=J&nace_r2=L68&nace_r2=M&nace_r2=N&indic_is=E_ERP1&lang=EN',
            nombre_archivo = 'empresas_erp_procesos_internos.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Empresas que tienen un sitio web o página de inicio'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ciwebn2?format=JSON&unit=PC_ENT&size_emp=GE10&nace_r2=C&nace_r2=E&nace_r2=F&nace_r2=G&nace_r2=H&nace_r2=I&nace_r2=ICT&nace_r2=J&nace_r2=M&nace_r2=N&nace_r2=L68&indic_is=E_WEB&lang=EN',
            nombre_archivo = 'empresas_presencia_web_propia.json',
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Empresas que utilizan el mercado de comercio electrónico para ventas'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ec_eseln2?format=JSON&unit=PC_ENT&size_emp=GE10&nace_r2=C&nace_r2=E&nace_r2=F&nace_r2=G&nace_r2=H&nace_r2=I&nace_r2=ICT&nace_r2=J&nace_r2=L68&nace_r2=M&nace_r2=N&indic_is=E_AESELL&lang=EN',
            nombre_archivo = 'empresas_venta_online.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Personas con habilidades digitales básicas'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_sk_dskl_i21?format=JSON&unit=PC_IND&ind_type=Y16_24&ind_type=Y25_64&ind_type=Y65_74&indic_is=I_DSK2_B&lang=en',
            nombre_archivo = 'habilidades_digitales_basicas.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Personas con habilidades digitales generales superiores a las básicas'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_sk_dskl_i21?format=JSON&unit=PC_IND&ind_type=Y16_24&ind_type=Y25_64&ind_type=Y65_74&indic_is=I_DSK2_AB&lang=en',
            nombre_archivo = 'habilidades_digitales_superior_a_basica.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Personas que interactúan en línea con las autoridades públicas'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ciegi_ac?format=JSON&unit=PC_IND&indic_is=I_IGOVANYS&ind_type=Y16_24&ind_type=Y25_64&ind_type=Y65_74&lang=en',
            nombre_archivo = 'interaccion_autoridades_publicas.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Usuarios que usan banca online'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ci_ac_i?format=JSON&unit=PC_IND_IU3&indic_is=I_IUBK&ind_type=Y16_24&ind_type=Y25_64&ind_type=Y65_74&lang=EN',
            nombre_archivo = 'personas_servicio_banca_electronica.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Uso regular de Internet'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ci_ifp_fu?format=JSON&unit=PC_IND_IU3&indic_is=I_IWK&ind_type=Y16_24&ind_type=Y25_64&ind_type=Y65_74&lang=EN',
            nombre_archivo = 'personas_uso_internet_una_vez_semana.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Empresas que utilizan las redes sociales'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_cismtn2?format=JSON&unit=PC_ENT&size_emp=GE10&nace_r2=C&nace_r2=E&nace_r2=F&nace_r2=G&nace_r2=H&nace_r2=I&nace_r2=ICT&nace_r2=J&nace_r2=L68&nace_r2=M&nace_r2=N&indic_is=E_SM1_ANY&lang=EN',
            nombre_archivo = 'empresas_uso_redes_sociales.json'
        ),
        Collector(
            indicador = CATALOGO_COMPLETO['Formación en TIC en empresas'],
            url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ske_ittn2?format=JSON&unit=PC_ENT&size_emp=GE10&nace_r2=C&nace_r2=E&nace_r2=F&nace_r2=G&nace_r2=H&nace_r2=I&nace_r2=ICT&nace_r2=J&nace_r2=L68&nace_r2=M&nace_r2=N&indic_is=E_ITT2&lang=EN',
            nombre_archivo = 'empresas_formacion_empleados_tic.json'
        )
    ]


def collector_eurostat():
    for indicador in FUENTES:
        indicador.recoger()  