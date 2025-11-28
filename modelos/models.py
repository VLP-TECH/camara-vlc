from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import pandas as pd

from microservicio_ingesta.scripts.processing.process_eurostat.process_all import process_data_eurostat, process_data_poblacion_por_edad
from microservicio_ingesta.scripts.processing.process_ine.process_all import process_data_ine
from microservicio_ingesta.scripts.processing.process_cnmc.process_all import process_data_cnmc, calcular_precio_mensual_cnmc
from microservicio_ingesta.scripts.processing.process_digital_decade.process_all import process_data_digital_decade

from microservicio_ingesta.scripts.ingestion.collect_ine.scrapping_pc_axis import descargar_tabla_por_id
from microservicio_ingesta.scripts.ingestion.collect_base.collect_api import collect_data_api
from microservicio_ingesta.scripts.ingestion.collect_base.collect_digital_decade import recoger_digital


class Dimension(Enum):
    # TODO HAY QUE CORREGIR LA ERRATA DE INOVACCIÓN
    EMPRENDIMIENTO_E_INNOVACION = 'Apoyo al emprendimiento e innovacción'
    CAPITAL_HUMANO = 'Capital humano'
    ECOSISTEMA_Y_COLABORACION = 'Ecosistema y colaboración'
    INFRAESTRUCTURA_DIGITAL = 'Infraestructura digital'
    SERVICIOS_PUBLICOS_DIGITALES = 'Servicios públicos digitales'
    SOSTENIBILIDAD_DIGITAL = 'Sostenibilidad digital'
    TRANSFORMACION_DIGITAL = 'Transformación digital empresarial'


class Subdimension(Enum):
    ACCESO_FINANCIACION = 'Acceso a financiación'
    DINAMISMO_EMPRENDEDOR = 'Dinamismo emprendedor'
    INFRAESTRUCTURA_APOYO = 'Infraestructura de apoyo'
    POLITICAS_FOMENTO = 'Políticas públicas de fomento'
    COMPETENCIAS_DIGITALES = 'Competencias digitales de la población'
    FORMACION_CONTINUA = 'Formación continua y reciclaje profesional'
    TALENTO_PROFESIONAL = 'Talento profesional TIC'
    ATRACTIVO_ECOSISTEMA = 'Atractivo y dinamismo del ecosistema'
    PROVISION_TECNOLOGICA = 'Entorno de provisión tecnológica'
    TRANSFERENCIA_CONOCIMIENTO = 'Transferencia de conocimiento'
    ACCESO_INFRAESTRUCTURAS = 'Acceso a infraestructuras'
    DISPONIBILIDAD_SERVICIOS_DIGITALES = 'Disponibilidad de servicios públicos digitales'
    INTEGRACION_ADMINISTRACION = 'Interacción digital con la administración'
    ECONOMIA_CIRCULAR = 'Economía circular y estrategias verdes'
    HUELLA_AMBIENTAL = 'Eficiencia y huella ambiental'
    ORGANIZACION_DIGITAL = 'Cultura de organización digital'
    DIGITALIZACION_BASICA = 'Digitalización básica'
    E_COMMERCE = 'E-commerce'
    TECNOLOGIAS_AVANZADAS = 'Tecnologías avanzadas'
    

class RolDato(Enum):
    NUMERADOR = "numerador"
    DENOMINADOR = "denominador"
    VALOR_A_ESCALAR = "valor_a_escalar"
    VALOR_BASE = "valor_base"
    MINIMO_ESCALA = "minimo_escala"
    MAXIMO_ESCALA = "maximo_escala"
    VALOR_A_AGREGAR = "valor_a_agregar"
    INDICE_A_PROMEDIAR = "indice_a_promediar"


@dataclass(frozen=True)
class Indicador:
    nombre: str
    dimension: Dimension
    subdimension: Subdimension
    origen: str
    importancia: str
    primer_anno: int | None = None
    formula_calculo: str | None = None
    datos: list | None = None
    fuente: str = 'Desconocida'
    

@dataclass
class Processor_base:
    nombre_archivo: str
    nombre_resultado: str

    ruta_datos_crudos: str = field(init=False)
    ruta_datos_unfiltered: str = field(init=False)
    ruta_datos_filtered: str = field(init=False)


    def __post_init__(self):
        # 1. Define las rutas base de forma robusta y reutilizable
        path_data = Path("data")
        path_fuente_procesada = path_data / "processed" / self._FUENTE

        # 2. Define la lógica para los nombres de fichero
        if self._FUENTE == 'cnmc':
            nombre_crudo = f'{self.origen}.{self._EXTENSION_CRUDOS}'
        else:
            nombre_crudo = f'{self.nombre_archivo}.{self._EXTENSION_CRUDOS}'

        nombre_unfiltered = f'{self.nombre_archivo}.{self._EXTENSION_UNFILTERED}'
        nombre_filtered = f'{self.nombre_archivo}.{self._EXTENSION_FILTERED}'

        # 3. Construye las rutas finales. pathlib se encarga de los separadores.
        self.ruta_datos_crudos = path_data / "raw" / self._FUENTE / nombre_crudo
        self.ruta_datos_unfiltered = path_fuente_procesada / "unfiltered" / nombre_unfiltered
        
        subcarpeta_filtered = "resultado" if self.procesado else "crudo"
        self.ruta_datos_filtered = path_fuente_procesada / "filtered" / subcarpeta_filtered / nombre_filtered


    def procesar(self):
        return {
            'ruta_archivo': str(self.ruta_datos_filtered),
            'nombre_indicador': self.indicador.nombre if self.indicador else None,
            'descripcion_dato': self.descripcion_dato if not self.procesado else None,
            'procesado': self.procesado if self.procesado else False,
            'nombre_resultado': self.nombre_resultado
        }

@dataclass
class Processor_digital_decade(Processor_base):
    indicador: Indicador | None = None
    procesado: bool | None = None
    descripcion_dato: str | None = None

    _FUENTE: str = 'digital_decade'
    _EXTENSION_CRUDOS: str = 'json'
    _EXTENSION_UNFILTERED: str = 'csv'
    _EXTENSION_FILTERED: str = 'csv'

    def procesar(self):
        process_data_digital_decade(
            self.ruta_datos_crudos, 
            self.ruta_datos_filtered,
            self.nombre_resultado
            )
        
        return super().procesar()

@dataclass
class Processor_eurostat(Processor_base):
    indicador: Indicador | None = None
    procesado: bool | None = None
    descripcion_dato: str | None = None

    _FUENTE: str = 'eurostat'
    _EXTENSION_CRUDOS: str = 'json'
    _EXTENSION_UNFILTERED: str = 'json'
    _EXTENSION_FILTERED: str = 'csv'

    def processar(self):
        process_data_eurostat(
            self.ruta_datos_crudos,
            self.ruta_datos_unfiltered,
            self.ruta_datos_filtered,
            self.nombre_resultado
        )

        return super().procesar()
    
    def depurar_datos_franjas_edad(self):
        process_data_poblacion_por_edad(
            self.ruta_datos_crudos,
            self.ruta_datos_unfiltered,
            self.ruta_datos_filtered,
            self.nombre_resultado
        )

        return super().procesar()
        


@dataclass
class Processor_ine(Processor_base):
    columnas: list
    filtros: list

    cambios_nombre: list | None = None
    indicador: Indicador | None = None
    procesado: bool | None = None
    descripcion_dato: str | None = None

    _FUENTE: str = 'ine'
    _EXTENSION_CRUDOS: str = 'px'
    _EXTENSION_UNFILTERED: str = 'px'
    _EXTENSION_FILTERED: str = 'csv'

    def procesar(self):
        process_data_ine(
            self.ruta_datos_crudos, 
            self.ruta_datos_unfiltered, 
            self.ruta_datos_filtered, 
            self.columnas, 
            self.filtros, 
            self.cambios_nombre,
            self.nombre_resultado,
        )

        return super().procesar()       


@dataclass
class Processor_cnmc(Processor_base):
    filtro: list
    origen: str
    agrupaciones: list

    descripcion_dato: str | None = None
    indicador: Indicador | None = None
    procesado: bool | None = None

    _FUENTE: str = 'cnmc'
    _EXTENSION_CRUDOS: str = 'json'
    _EXTENSION_UNFILTERED: str = 'csv'
    _EXTENSION_FILTERED: str = 'csv'

    def procesar(self):
        process_data_cnmc(
            self.ruta_datos_crudos,
            self.ruta_datos_unfiltered,
            self.ruta_datos_filtered,
            self.filtro,
            self.agrupaciones,
            self.nombre_resultado
        )

        return super().procesar()
    
    def obtener_precio_mensual(self):
        calcular_precio_mensual_cnmc(
            self.ruta_datos_crudos,
            self.ruta_datos_unfiltered,
            self.ruta_datos_filtered,
            self.filtro,
            self.agrupaciones,
            self.nombre_resultado
        )

        return super().procesar()

@dataclass
class Processor_macro(Processor_base):
    descripcion_dato: str | None = None
    indicador: Indicador | None = None
    procesado: bool | None = None
    nombre_antiguo: str | None = None

    _FUENTE: str = 'WorldBank'
    _EXTENSION_CRUDOS: str = 'csv'
    _EXTENSION_UNFILTERED: str = 'csv'
    _EXTENSION_FILTERED: str = 'csv'

    # Check a esta función por semi-inutilidad
    def procesar(self):
        df = pd.read_csv(self.ruta_datos_crudos)
        df = df.rename(columns={self.nombre_antiguo: self.nombre_resultado, 'Año': 'periodo'})
        df['Euros'] = df['Euros'] / 12
        df.to_csv(self.ruta_datos_filtered)
        return super().procesar()


@dataclass
class Collector_base:
    url: str
    nombre_archivo: str
    ruta_datos_crudos: str | None = None
    indicador: Indicador | None = None

    def recoger(self):
        collect_data_api(
            self.url,
            self.nombre_archivo,
            self.ruta_datos_crudos
        )


@dataclass
class Collector_ine():
    id: str
    nombre_archivo: str
    tipo_tabla: str
    ruta_datos_crudos: str | None = None
    indicador: Indicador | None = None

    def __post_init__(self):
        self.ruta_datos_crudos = Path("data") / "raw" / "ine"

    def recoger(self):
        descargar_tabla_por_id(
            self.id,
            self.nombre_archivo,
            self.ruta_datos_crudos,
            self.tipo_tabla
        )

@dataclass
class Collector_digital_decade:
    url: str
    nombre_archivo: str
    indicador: Indicador | None = None
    empresa: bool | None = False
    extension: str = '.json'

    def __post_init__(self):
        self.ruta_datos_crudos = Path("data") / "raw" / "digital_decade"
        self.nombre_archivo += self.extension

    def recoger(self):
        recoger_digital(self.empresa, self.url, self.ruta_datos_crudos, self.nombre_archivo)

@dataclass
class Collector_eurostat(Collector_base):
    def __post_init__(self):
        self.ruta_datos_crudos = Path("data") / "raw" / "eurostat"
    
@dataclass
class Colletor_cnmc(Collector_base):
    def __post_init__(self):
        self.ruta_datos_crudos = Path("data") / "raw" / "cnmc"
