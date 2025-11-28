from sqlalchemy import Column, Integer, String, Numeric
from database.connection import Base
from sqlalchemy.orm import relationship

class DatoMacro(Base):
    __tablename__ = 'datos_macro'

    id = Column(Integer, primary_key=True)

    descripcion_dato = Column(String(200))
    unidad = Column(String(40))
    valor = Column(Numeric(20, 2))

    periodo = Column(Integer)
    pais = Column(String(100))
    provincia = Column(String(100))
    tamano_empresa = Column(String(100))
    sector = Column(String(200))

    dato_macro_procesado = relationship('ProcessedDatoMacro', back_populates='dato_macro_origen')