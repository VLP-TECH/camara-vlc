from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database.connection import Base
from modelos.models import Dimension as DimensionEnum

class Dimension(Base):
    __tablename__ = 'dimensiones'   

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    peso = Column(Integer, nullable=False)

    subdimensiones = relationship('Subdimension', back_populates='dimension')