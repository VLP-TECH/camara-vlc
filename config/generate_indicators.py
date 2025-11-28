from modelos.models import Indicador, Dimension, Subdimension
import pandas as pd
import re

MAPEO_DIMENSION = {
    'Apoyo al emprendimiento e innovacción': Dimension.EMPRENDIMIENTO_E_INNOVACION,
    'Capital humano': Dimension.CAPITAL_HUMANO,
    'Ecosistema y colaboración': Dimension.ECOSISTEMA_Y_COLABORACION,
    'Infraestructura digital': Dimension.INFRAESTRUCTURA_DIGITAL,
    'Servicios públicos digitales': Dimension.SERVICIOS_PUBLICOS_DIGITALES,
    'Sostenibilidad digital': Dimension.SOSTENIBILIDAD_DIGITAL,
    'Transformación digital empresarial': Dimension.TRANSFORMACION_DIGITAL
}

MAPEO_SUBDIMENSION = {
    'Acceso a financiación': Subdimension.ACCESO_FINANCIACION,
    'Dinamismo emprendedor': Subdimension.DINAMISMO_EMPRENDEDOR,
    'Infraestructura de apoyo': Subdimension.INFRAESTRUCTURA_APOYO,
    'Políticas públicas de fomento': Subdimension.POLITICAS_FOMENTO,
    'Competencias digitales de la población': Subdimension.COMPETENCIAS_DIGITALES,
    'Formación continua y reciclaje profesional': Subdimension.FORMACION_CONTINUA,
    'Talento profesional TIC': Subdimension.TALENTO_PROFESIONAL,
    'Atractivo y dinamismo del ecosistema': Subdimension.ATRACTIVO_ECOSISTEMA,
    'Entorno de provisión tecnológica': Subdimension.PROVISION_TECNOLOGICA,
    'Transferencia de conocimiento': Subdimension.TRANSFERENCIA_CONOCIMIENTO,
    'Acceso a infraestructuras': Subdimension.ACCESO_INFRAESTRUCTURAS,
    'Disponibilidad de servicios públicos digitales': Subdimension.DISPONIBILIDAD_SERVICIOS_DIGITALES,
    'Interacción digital con la administración': Subdimension.INTEGRACION_ADMINISTRACION,
    'Economía circular y estrategias verdes': Subdimension.ECONOMIA_CIRCULAR,
    'Eficiencia y huella ambiental': Subdimension.HUELLA_AMBIENTAL,
    'Cultura de organización digital': Subdimension.ORGANIZACION_DIGITAL,
    'Digitalización básica': Subdimension.DIGITALIZACION_BASICA,
    'E-commerce': Subdimension.E_COMMERCE,
    'Tecnologías avanzadas': Subdimension.TECNOLOGIAS_AVANZADAS
}

def obtener_primer_anno_deseado(texto_periocidad):
    annos_encontrados = re.findall(r'\b\d{4}\b', texto_periocidad)

    if not annos_encontrados:
        return None
    
    annos_numericos = [int(anno) for anno in annos_encontrados]

    return min(annos_numericos)

def generar_fichero_indicadores():
    df_indicadores = pd.read_excel('data/raw/indicadores/sistema_de_indicadores.xlsx')

    output_path = 'data/processed/indicadores/indicators.py'

    file_content = """# -*- coding: utf-8 -*-
# ¡ATENCIÓN! ESTE ARCHIVO ES GENERADO AUTOMÁTICAMENTE.
# NO LO EDites A MANO. EJECUTA build_indicators.py PARA ACTUALIZARLO.

from modelos.models import Indicador, Dimension, Subdimension

CATALOGO_COMPLETO = {
    """

    for _, row in df_indicadores.iterrows():
        dimension_excel = row['Dimensión'].strip()
        subdimension_excel = row['Subdimensión'].strip()

        dimension_enum = MAPEO_DIMENSION.get(dimension_excel)
        subdimension_enum = MAPEO_SUBDIMENSION.get(subdimension_excel)

        if not dimension_enum or not subdimension_enum:
            print(f'No se encontró mapeo para {dimension_excel} o {subdimension_excel}')

            continue

        datos_list = [
            linea.strip() for linea in str(row['Datos']).replace('•', '').split('\n') if linea.strip()
        ]        
        
        periocidad_valor = row['Periocidad']
        anno_min = None if pd.isna(periocidad_valor) else obtener_primer_anno_deseado(str(periocidad_valor))

        file_content += f"""   
    "{row['Indicador'].replace('"', "'").strip()}": Indicador(
        nombre="{row['Indicador'].replace('"', "'").strip()}",
        dimension=Dimension.{dimension_enum.name},
        subdimension=Subdimension.{subdimension_enum.name},
        origen ="{row['Origen indicador']}",
        importancia ="{row['Importancia']}",
        fuente ="{row['Fuente']}",
        formula_calculo ="{row['Formula de cálculo']}",
        datos ={datos_list},
        primer_anno ={anno_min}
        ),\n"""

    file_content += '''
    }\n
    '''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    

if __name__ == '__main__':
    generar_fichero_indicadores()