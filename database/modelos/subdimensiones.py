from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.connection import Base
from modelos.models import Subdimension as SubdimensionEnum

class Subdimension(Base):
    __tablename__ = 'subdimensiones'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    peso = Column(Integer, nullable=False)
    id_dimension = Column(Integer, ForeignKey('dimensiones.id'))

    dimension = relationship('Dimension', back_populates='subdimensiones')
    indicadores = relationship('DefinicionIndicador', back_populates='subdimension')