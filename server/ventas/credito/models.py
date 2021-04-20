from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from server.ventas.cuota.models import *

from ...database.models import Base
from server.database.serializable import Serializable



class Credito(Serializable, Base):
    way = {'moneda': {},'contratos': {},'estadocredito': {},'entidad': {},'cuotas': {'estadocuota': {}}}

    __tablename__ = 'credito'

    id = Column( Integer, primary_key=True)
    numeroCuotas = Column( Integer, nullable=False)
    capital = Column( Float, nullable=False)
    fkmoneda = Column(Integer, ForeignKey('moneda.id'), nullable=True)
    fkentidad = Column(Integer, ForeignKey('entidad.id'), nullable=True)
    fkestadocredito = Column(Integer, ForeignKey('estadoCredito.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    estadocredito = relationship('Estadocredito')
    entidad = relationship('Entidad')
    cuotas = relationship('Cuota', cascade="save-update, merge, delete, delete-orphan")
    contratos = relationship('Contrato')
    moneda = relationship('Moneda')

    # def get_dict(self, way=None):
    #     aux = super().get_dict(way)
    #
    #     aux['nombreCliente'] = self.contratos[0].reserva.cliente.fullname
    #
    #     return aux



class Estadocredito(Serializable, Base):
    way = {}

    __tablename__ = 'estadoCredito'

    id = Column( Integer, primary_key=True)
    nombre = Column(  String(100), nullable=False)

    enabled = Column(Boolean, default=True)

