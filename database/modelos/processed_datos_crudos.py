from sqlalchemy import (Column, Integer, String, ForeignKey, Numeric, Boolean, DATE)
from sqlalchemy.orm import relationship
from database.connection import Base
from database.modelos.resultados_indicadores import resultados_fuente_crudo


class ProcessedDatoCrudo(Base):
    """
    Almacena los datos crudos una vez que han sido limpiados, 
    validados y normalizados.
    """
    __tablename__ = 'processed_datos_crudos'

    id = Column(Integer, primary_key=True)
    
    id_dato_crudo = Column(Integer, ForeignKey('datos_crudos.id'), nullable=False, unique=True)
    
    descripcion_dato = Column(String(200))
    valor = Column(Numeric(20, 2))
    unidad_tipo = Column(String(50))
    unidad_display = Column(String(80))

    periodo = Column(DATE)
    pais = Column(String(100))
    provincia = Column(String(100))
    tamano_empresa = Column(String(100))
    sector = Column(String(300))

    procesado = Column(Boolean)

    
    dato_crudo_origen = relationship('DatoCrudo', back_populates='dato_crudo_procesado')
    resultados = relationship('ResultadoIndicador', secondary=resultados_fuente_crudo, back_populates='origen_crudo')    