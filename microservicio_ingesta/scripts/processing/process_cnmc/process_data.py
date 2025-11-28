from modelos.models import Processor_cnmc as Processor
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

DATOS = [
        Processor(
            indicador = CATALOGO_COMPLETO['Adopción de banda ancha móvil (suscripciones/100 personas)'],
            origen = 'telecomunicaciones',
            nombre_archivo = 'suscripciones_datos_moviles',
            filtro = ['servicio', 'Telefonía móvil'],
            agrupaciones = ['anno', 'provincia'],
            nombre_resultado = 'lineas_o_accesos',
            descripcion_dato = 'Nº total de suscripciones activas de datos móviles'
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Adopción de banda ancha fija (suscripciones/100 personas)'],
            origen = 'telecomunicaciones',
            nombre_archivo = 'suscripciones_banda_ancha_fija',
            filtro = ['servicio', 'Banda ancha fija'],
            agrupaciones = ['anno', 'provincia'],
            nombre_resultado = 'lineas_o_accesos',
            descripcion_dato = 'Nº total de suscripciones de banda ancha fija'
        )
        
    ]


def processor_cnmc():
    datos_insercion = []
    for indicador in DATOS:
        datos_insercion.append(indicador.procesar())

    ingresos_mensuales = Processor(
            indicador = CATALOGO_COMPLETO['Precio relativo de banda ancha'],
            origen = 'ingresos',
            nombre_archivo = 'precio_banda_ancha',
            filtro = ['tipo_de_ingreso', 'Banda ancha fija'],
            agrupaciones = ['anno', 'pais'],
            nombre_resultado = 'ingresos',
            descripcion_dato = 'Precio mensual del servicio de banda ancha en euros'
        )
    
    datos_insercion.append(ingresos_mensuales.obtener_precio_mensual())

    return datos_insercion

if __name__ == '__main__':
    processor_cnmc