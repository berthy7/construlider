from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Terreno(Serializable, Base):
    way = {'manzano': {'urbanizacion': {}}}

    __tablename__ = 'terreno'

    id = Column( Integer, primary_key=True)
    ancho = Column( Float, nullable=False)
    largo = Column( Float, nullable=False)
    superficie = Column(Float, nullable=False)
    superficieConstruida = Column(Float, nullable=True)

    fkmanzano = Column(Integer, ForeignKey('manzano.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    manzano = relationship('Manzano')

