from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class DatoCrudo(Base):
    __tablename__ = 'datos_crudos'

    id = Column(Integer, primary_key=True)

    id_indicador = Column(Integer, ForeignKey('definiciones_indicadores.id'))

    descripcion_dato = Column(String(200))
    unidad = Column(String(40))
    valor = Column(Numeric(20, 2))

    periodo = Column(Integer)
    pais = Column(String(100))
    provincia = Column(String(100))
    tamano_empresa = Column(String(100))
    sector = Column(String(300))

    procesado = Column(Boolean, default=False)

    indicador = relationship('DefinicionIndicador', back_populates='datos_crudos')
    dato_crudo_procesado = relationship('ProcessedDatoCrudo', back_populates='dato_crudo_origen', uselist=False)

    __table_args__ = (
        UniqueConstraint('id_indicador', 'provincia', 'pais', 'periodo', 'tamano_empresa', 'sector', name='uq_dato_crudo_conceptual'),
    )