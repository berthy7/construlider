from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Terreno(Serializable, Base):
    way = {'moneda': {},'manzano': {},'tipoterreno': {}}

    __tablename__ = 'terreno'

    id = Column( Integer, primary_key=True)
    norte = Column( Float, nullable=False)
    sur = Column( Float, nullable=True)
    este = Column( Float, nullable=True)
    oeste = Column( Float, nullable=True)
    superficie = Column(Float, nullable=False)
    superficieConstruida = Column(Float, nullable=True)
    valorMetroCuadrado = Column(Float, nullable=True)
    fkmoneda = Column(Integer, ForeignKey('moneda.id'), nullable=True)
    foto1 = Column(Text, nullable=True)
    foto2 = Column(Text, nullable=True)
    foto3 = Column(Text, nullable=True)
    foto4 = Column(Text, nullable=True)

    fkmanzano = Column(Integer, ForeignKey('manzano.id'), nullable=True)
    fktipoterreno = Column(Integer, ForeignKey('tipoTerreno.id'), nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    moneda = relationship('Moneda')
    manzano = relationship('Manzano')
    tipoterreno = relationship('Tipoterreno')


class Tipoterreno(Serializable, Base):
    way = {}

    __tablename__ = 'tipoTerreno'

    id = Column( Integer, primary_key=True)
    nombre = Column(  String(100), nullable=False)

    enabled = Column(Boolean, default=True)


