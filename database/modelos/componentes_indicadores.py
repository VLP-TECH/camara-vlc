from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from database.connection import Base
from modelos.models import RolDato
from enum import Enum as pyEnum

componentes_resultados = Table(
    "componentes_resultados",
    Base.metadata,
    Column("id_componente", Integer, ForeignKey("componentes_indicadores.id")),
    Column("id_resultado", Integer, ForeignKey("resultados_indicadores.id"))
)

class FUENTES_TABLAS(pyEnum):
    DATOS_CRUDOS = 'processed_datos_crudos'
    DATOS_MACRO = 'processed_datos_macro'

class ComponenteIndicador(Base):
    __tablename__ = 'componentes_indicadores'

    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey('definiciones_indicadores.id', ondelete='CASCADE'))
    descripcion_dato = Column(String(200))
    fuente = Column(Enum(FUENTES_TABLAS))
    rol = Column(Enum(RolDato, native_enum=False), nullable=False)

    indicador = relationship('DefinicionIndicador', back_populates='componentes')
    resultados = relationship('ResultadoIndicador', secondary=componentes_resultados, back_populates='componente')