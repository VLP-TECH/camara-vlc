from sqlalchemy import (Column, Integer, String, ForeignKey, Numeric, Boolean, DATE)
from sqlalchemy.orm import relationship
from database.connection import Base
from database.modelos.resultados_indicadores import resultados_fuente_macro

class ProcessedDatoMacro(Base):
    """
    Almacena los datos macro una vez que han sido limpiados, 
    validados y normalizados.
    """
    __tablename__ = 'processed_datos_macro'

    id = Column(Integer, primary_key=True)
    
    id_dato_macro = Column(Integer, ForeignKey('datos_macro.id'), nullable=False, index=True)

    descripcion_dato = Column(String(200))
    valor = Column(Numeric(20, 2))
    unidad_tipo = Column(String(50))
    unidad_display = Column(String(80))

    periodo = Column(DATE)
    pais = Column(String(100))
    provincia = Column(String(100))
    tamano_empresa = Column(String(100))
    sector = Column(String(200))

    
    dato_macro_origen = relationship('DatoMacro', back_populates='dato_macro_procesado')
    resultados = relationship('ResultadoIndicador', secondary=resultados_fuente_macro, back_populates='origen_macro')