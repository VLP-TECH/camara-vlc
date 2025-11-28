from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DATE
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from database.modelos.componentes_indicadores import componentes_resultados
from sqlalchemy import Table, CheckConstraint

resultados_fuente_crudo = Table(
    'resultados_fuente_crudo',
    Base.metadata,
    Column('id_resultado', Integer, ForeignKey('resultados_indicadores.id'), primary_key=True),
    Column('id_dato_crudo', Integer, ForeignKey('processed_datos_crudos.id'), primary_key=True)
)

resultados_fuente_macro = Table(
    'resultados_fuente_macro',
    Base.metadata,
    Column('id_resultado', Integer, ForeignKey('resultados_indicadores.id'), primary_key=True),
    Column('id_dato_macro', Integer, ForeignKey('processed_datos_macro.id'), primary_key=True)
)


class ResultadoIndicador(Base):
    """
    Almacena el resultado final de un indicador calculado a partir 
    de los datos ya procesados.
    """
    __tablename__ = 'resultados_indicadores'
    
    id = Column(Integer, primary_key=True)
    
    valor_calculado = Column(Numeric(20, 6), nullable=False)
    fecha_calculo = Column(DATE, server_default=func.now())

    unidad_tipo = Column(String(50))
    unidad_display = Column(String(80))

    periodo = Column(DATE)
    pais = Column(String(100))
    provincia = Column(String(100))
    sector = Column(String(300))
    tamano_empresa = Column(String(100))

    componente = relationship('ComponenteIndicador', secondary=componentes_resultados, back_populates='resultados')
    origen_crudo = relationship('ProcessedDatoCrudo', secondary=resultados_fuente_crudo, back_populates='resultados')
    origen_macro = relationship('ProcessedDatoMacro', secondary=resultados_fuente_macro, back_populates='resultados')