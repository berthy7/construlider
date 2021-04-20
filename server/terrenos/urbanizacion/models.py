from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Urbanizacion(Serializable, Base):
    way = {'moneda': {},'manzanos': {}}

    __tablename__ = 'urbanizacion'

    id = Column( Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column( String(100), nullable=False)
    uv = Column(String(100), nullable=False)
    numeroTerrenos = Column( Integer, nullable=False)
    numeroCasas = Column(Integer, nullable=False)
    numeroManzanos = Column(Integer, nullable=False)
    valorMetroCuadrado = Column(Float, nullable=True)
    fkmoneda = Column(Integer, ForeignKey('moneda.id'), nullable=True)


    enabled = Column(Boolean, default=True)

    moneda = relationship('Moneda')
    manzanos = relationship('Manzano', cascade="save-update, merge, delete, delete-orphan")

