from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable



class Reserva(Serializable, Base):
    way = {'cliente': {},'moneda': {},'terreno': {'manzano': {'urbanizacion': {}},'tipoterreno': {}},'estadoreserva': {}}

    __tablename__ = 'reserva'

    id = Column( Integer, primary_key=True)
    monto = Column( Float, nullable=True)
    fechaReserva = Column( Date, nullable=False)
    fechaDevolucion = Column(Date, nullable=True)

    fkcliente = Column(Integer, ForeignKey('cliente.id'), nullable=True)
    fkterreno = Column(Integer, ForeignKey('terreno.id'), nullable=True)
    fkestadoreserva = Column(Integer, ForeignKey('estadoReserva.id'), nullable=True)
    fkmoneda = Column(Integer, ForeignKey('moneda.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    cliente = relationship('Cliente')
    terreno = relationship('Terreno')
    estadoreserva = relationship('Estadoreserva')
    moneda = relationship('Moneda')



    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechaReserva'] == 'None':
            aux['fechaReserva'] = None
        else:
            aux['fechaReserva'] = self.fechaReserva.strftime('%d/%m/%Y')

        if aux['fechaDevolucion'] == 'None':
            aux['fechaDevolucion'] = None
        else:
            aux['fechaDevolucion'] = self.fechaDevolucion.strftime('%d/%m/%Y')

        return aux



class Estadoreserva(Serializable, Base):
    way = {}

    __tablename__ = 'estadoReserva'

    id = Column( Integer, primary_key=True)
    nombre = Column(String(100), nullable=False) #Iniciado,Contrato,pagado,Cancelado

    enabled = Column(Boolean, default=True)

