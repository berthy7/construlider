from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from ...database.models import Base
from server.database.serializable import Serializable



class Ajuste(Serializable, Base):
    way = {'monedaReserva': {}}

    __tablename__ = 'ajuste'

    id = Column( Integer, primary_key=True)
    montoMinimoReserva = Column( Float, nullable=False)
    fkmonedaReserva = Column(Integer, ForeignKey('moneda.id'), nullable=True)
    tasaInteres = Column(Float, nullable=True)
    cuotasMora = Column(Integer, nullable=True)

    enabled = Column(Boolean, default=True)

    monedaReserva = relationship('Moneda')
