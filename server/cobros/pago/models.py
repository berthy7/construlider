from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from ...database.models import Base
from server.database.serializable import Serializable


class Pago(Serializable, Base):
    way = {'moneda': {},'tipopago': {},'cuota': {}}

    __tablename__ = 'pago'

    id = Column( Integer, primary_key=True)
    monto = Column( Float, nullable=False)
    fkmoneda = Column(Integer, ForeignKey('moneda.id'), nullable=True)
    fecha = Column( Date, nullable=False)
    fotoComprobante = Column(Text, nullable=True)
    fkcuota = Column(Integer, ForeignKey('cuota.id'), nullable=True)
    fktipopago = Column(Integer, ForeignKey('tipoPago.id'), nullable=True)

    enabled = Column(Boolean, default=True)
    tipopago = relationship('Tipopago')
    cuota = relationship('Cuota')
    moneda = relationship('Moneda')


class Tipopago(Serializable, Base):
    way = {}

    __tablename__ = 'tipoPago'

    id = Column( Integer, primary_key=True)
    nombre = Column(  String(100), nullable=False)

    enabled = Column(Boolean, default=True)
