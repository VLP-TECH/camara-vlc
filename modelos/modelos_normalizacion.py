from enum import Enum

class PaisesEuropa(Enum):
    """
    Enumeración que representa los países de Europa.
    
    Los nombres de los miembros están normalizados en mayúsculas (p.ej., REPUBLICA_CHECA),
    mientras que sus valores conservan el formato original (p.ej., 'República Checa').
    """
    ALEMANIA = 'Alemania'
    ALBANIA = 'Albania'
    ANDORRA = 'Andorra'
    AUSTRIA = 'Austria'
    BELGICA = 'Bélgica'
    BIELORRUSIA = 'Bielorrusia'
    BOSNIA_Y_HERZEGOVINA = 'Bosnia y Herzegovina'
    BULGARIA = 'Bulgaria'
    CHIPRE = 'Chipre'
    CROACIA = 'Croacia'
    DINAMARCA = 'Dinamarca'
    ESLOVAQUIA = 'Eslovaquia'
    ESLOVENIA = 'Eslovenia'
    ESPAÑA = 'España'
    ESTONIA = 'Estonia'
    FINLANDIA = 'Finlandia'
    FRANCIA = 'Francia'
    GRECIA = 'Grecia'
    HUNGRIA = 'Hungría'
    IRLANDA = 'Irlanda'
    ICELAND = 'Iceland'
    ITALIA = 'Italia'
    KOSOVO = 'Kosovo'
    LETONIA = 'Letonia'
    LIECHTENSTEIN = 'Liechtenstein'
    LITUANIA = 'Lituania'
    LUXEMBURGO = 'Luxemburgo'
    MACEDONIA_DEL_NORTE = 'Macedonia del Norte'
    MALTA = 'Malta'
    MOLDAVIA = 'Moldavia'
    MONACO = 'Mónaco'
    MONTENEGRO = 'Montenegro'
    NORUEGA = 'Noruega'
    PAISES_BAJOS = 'Países Bajos'
    POLONIA = 'Polonia'
    PORTUGAL = 'Portugal'
    REINO_UNIDO = 'Reino Unido'
    REPUBLICA_CHECA = 'República Checa'
    RUMANIA = 'Rumanía'
    RUSIA = 'Rusia'
    SAN_MARINO = 'San Marino'
    SERBIA = 'Serbia'
    SUECIA = 'Suecia'
    SUIZA = 'Suiza'
    TURQUIA = 'Turquía'
    UCRANIA = 'Ucrania'
    VATICANO = 'Vaticano'


class ProvinciasEspana(Enum):
    """
    Enumeración que representa las provincias y ciudades autónomas de España.
    
    Los nombres de los miembros están normalizados en mayúsculas (p.ej., A_CORUNA),
    mientras que sus valores conservan el formato y ortografía oficial (p.ej., 'A Coruña').
    """
    A_CORUNA = 'A Coruña'
    ALAVA = 'Álava'
    ALBACETE = 'Albacete'
    ALICANTE = 'Alicante'
    ALMERIA = 'Almería'
    ASTURIAS = 'Asturias'
    AVILA = 'Ávila'
    BADAJOZ = 'Badajoz'
    BARCELONA = 'Barcelona'
    BIZKAIA = 'Bizkaia'
    BURGOS = 'Burgos'
    CACERES = 'Cáceres'
    CADIZ = 'Cádiz'
    CANTABRIA = 'Cantabria'
    CASTELLON = 'Castellón'
    CEUTA = 'Ceuta'
    CIUDAD_REAL = 'Ciudad Real'
    CORDOBA = 'Córdoba'
    CUENCA = 'Cuenca'
    GIPUZKOA = 'Gipuzkoa'
    GIRONA = 'Girona'
    GRANADA = 'Granada'
    GUADALAJARA = 'Guadalajara'
    HUELVA = 'Huelva'
    HUESCA = 'Huesca'
    ILLES_BALEARS = 'Illes Balears'
    JAEN = 'Jaén'
    LA_RIOJA = 'La Rioja'
    LAS_PALMAS = 'Las Palmas'
    LEON = 'León'
    LLEIDA = 'Lleida'
    LUGO = 'Lugo'
    MADRID = 'Madrid'
    MALAGA = 'Málaga'
    MELILLA = 'Melilla'
    MURCIA = 'Murcia'
    NAVARRA = 'Navarra'
    OURENSE = 'Ourense'
    PALENCIA = 'Palencia'
    PONTEVEDRA = 'Pontevedra'
    SALAMANCA = 'Salamanca'
    SANTA_CRUZ_DE_TENERIFE = 'Santa Cruz de Tenerife'
    SEGOVIA = 'Segovia'
    SEVILLA = 'Sevilla'
    SORIA = 'Soria'
    TARRAGONA = 'Tarragona'
    TERUEL = 'Teruel'
    TOLEDO = 'Toledo'
    VALENCIA = 'Valencia'
    VALLADOLID = 'Valladolid'
    ZAMORA = 'Zamora'
    ZARAGOZA = 'Zaragoza'

class SectoresEconomicos(Enum):
    """
    Enumeración que representa los sectores económicos basados en la NACE
    y otras agregaciones comunes.
    
    Los nombres de los miembros están normalizados en mayúsculas (p.ej., TOTAL_INDUSTRIA),
    mientras que sus valores conservan el formato original y descriptivo 
    (p.ej., 'Total Industria').
    """
    ACTIVIDADES_ADMINISTRATIVAS_Y_SERVICIOS_AUXILIARES = 'Actividades administrativas y servicios auxiliares'
    ACTIVIDADES_INMOBILIARIAS = 'Actividades inmobiliarias'
    ACTIVIDADES_PROFESIONALES_CIENTIFICAS_Y_TECNICAS = 'Actividades profesionales, científicas y técnicas'
    COMERCIO_Y_REPARACION_DE_VEHICULOS = 'Comercio y reparación de vehículos'
    CONSTRUCCION = 'Construcción'
    HOSTELERIA_Y_SERVICIOS_DE_COMIDA = 'Hostelería y servicios de comida'
    INDUSTRIA_DE_ALIMENTACION_TEXTIL_Y_MADERA = 'Industria de alimentación, textil y madera'
    INDUSTRIA_DE_MAQUINARIA_Y_EQUIPO_TECNOLOGICO = 'Industria de maquinaria y equipo tecnológico'
    INDUSTRIA_MANUFACTURERA = 'Industria manufacturera'
    INDUSTRIA_METALURGICA = 'Industria metalúrgica'
    INDUSTRIA_QUIMICA_FARMACEUTICA_Y_MINERAL = 'Industria química, farmacéutica y mineral'
    INFORMACION_Y_COMUNICACIONES = 'Información y comunicaciones'
    SECTOR_TIC = 'Sector TIC'
    SUMINISTRO_DE_ENERGIA_Y_AGUA = 'Suministro de energía y agua'
    TOTAL_CONSTRUCCION = 'Total Construcción'
    TOTAL_EMPRESAS = 'Total Empresas'
    TOTAL_INDUSTRIA = 'Total Industria'
    TOTAL_SERVICIOS = 'Total Servicios'
    TRANSPORTE_Y_ALMACENAMIENTO = 'Transporte y almacenamiento'

class TamanosEmpresa(Enum):
    """
    Enumeración que representa los tamaños de empresa según el número de personas empleadas.
    
    Los nombres de los miembros están normalizados en mayúsculas (p.ej., PERSONAS_0_A_9),
    mientras que sus valores conservan el formato original (p.ej., '0-9 personas').
    """
    PERSONAS_0_A_9 = '0-9 personas'
    PERSONAS_10_A_49 = '10-49 personas'
    PERSONAS_10_O_MAS = '10+ personas'
    PERSONAS_250_O_MAS = '250+ personas'
    PERSONAS_50_A_249 = '50-249 personas'
    TOTAL = 'Total'