from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Terreno(Serializable, Base):
    way = {'manzano': {'contrato': {}}}

    __tablename__ = 'terreno'

    id = Column( Integer, primary_key=True)
    ancho = Column( Float, nullable=False)
    largo = Column( Float, nullable=False)
    superficie = Column(Float, nullable=False)
    superficieConstruida = Column(Float, nullable=True)

    fkmanzano = Column(Integer, ForeignKey('manzano.id'), nullable=True)
    fktipoterreno = Column(Integer, ForeignKey('tipoTerreno.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    manzano = relationship('Manzano')
    tipoterreno = relationship('Tipoterreno')


class Tipoterreno(Serializable, Base):
    way = {}

    __tablename__ = 'tipoTerreno'

    id = Column( Integer, primary_key=True)
    nombre = Column(  String(100), nullable=False)

    enabled = Column(Boolean, default=True)


