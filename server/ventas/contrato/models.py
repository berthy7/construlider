from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Contrato(Serializable, Base):
    way = {'reserva': {'cliente': {}},'credito': {'cuotas': {}},'moneda': {},'tipoventa': {}}

    __tablename__ = 'contrato'

    id = Column( Integer, primary_key=True)
    fecha = Column( DateTime, nullable=False)
    monto = Column( Float, nullable=True)
    fkmoneda = Column(Integer, ForeignKey('moneda.id'), nullable=True)
    numeroCuotas = Column(Integer, nullable=True)
    cuotaInicial = Column(Float, nullable=True)
    fechaPrimerCuota = Column(Date, nullable=True)

    fkreserva = Column(Integer, ForeignKey('reserva.id'), nullable=True)
    fkcredito = Column(Integer, ForeignKey('credito.id'), nullable=True)
    fktipoventa = Column(Integer, ForeignKey('tipoVenta.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    reserva = relationship('Reserva')
    credito = relationship('Credito')
    tipoventa = relationship('Tipoventa')
    moneda = relationship('Moneda')


    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fecha'] == 'None':
            aux['fecha'] = None
        else:
            aux['fecha'] = self.fecha.strftime('%d/%m/%Y')

        if aux['fechaPrimerCuota'] == 'None':
            aux['fechaPrimerCuota'] = None
        else:
            aux['fechaPrimerCuota'] = self.fechaPrimerCuota.strftime('%d/%m/%Y')

        return aux


class Tipoventa(Serializable, Base):
    way = {}

    __tablename__ = 'tipoVenta'

    id = Column( Integer, primary_key=True)
    nombre = Column(String(100), nullable=False) #contado,credito

    enabled = Column(Boolean, default=True)


