from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Urbanizacion(Serializable, Base):
    way = {'manzanos': {}}

    __tablename__ = 'urbanizacion'

    id = Column( Integer, primary_key=True)
    direccion = Column( String(100), nullable=False)
    numeroTerrenos = Column( Integer, nullable=False)
    numeroCasas = Column(Integer, nullable=False)
    numeroManzanos = Column(Integer, nullable=False)

    enabled = Column(Boolean, default=True)

    manzanos = relationship('Manzano', cascade="save-update, merge, delete, delete-orphan")

