from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class DefinicionIndicador(Base):
    __tablename__ = 'definiciones_indicadores'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    id_subdimension = Column(Integer, ForeignKey('subdimensiones.id'))
    origen_indicador = Column(String(50))
    formula = Column(String(20), nullable=False)
    importancia = Column(String(10), nullable=False)
    fuente = Column(String(200))

    subdimension = relationship('Subdimension', back_populates='indicadores')
    componentes = relationship('ComponenteIndicador', back_populates='indicador')
    datos_crudos = relationship('DatoCrudo', back_populates='indicador')
