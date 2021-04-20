from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Cuota(Serializable, Base):
    way = {'moneda': {},'credito': {},'estadocuota': {},'pagos': {}}

    __tablename__ = 'cuota'

    id = Column( Integer, primary_key=True)
    numero = Column(Integer, nullable=False)
    monto = Column( Float, nullable=False)
    fkmoneda = Column(Integer, ForeignKey('moneda.id'), nullable=True)
    fechaVencimiento = Column( Date, nullable=False)
    fkcredito = Column(Integer, ForeignKey('credito.id'), nullable=True)
    fkestadocuota = Column(Integer, ForeignKey('estadoCuota.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    credito = relationship('Credito')
    moneda = relationship('Moneda')
    estadocuota = relationship('Estadocuota')
    pagos = relationship('Pago', cascade="save-update, merge, delete, delete-orphan")

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fechaVencimiento'] == 'None':
            aux['fechaVencimiento'] = None
        else:
            aux['fechaVencimiento'] = self.fechaVencimiento.strftime('%d/%m/%Y')

        return aux



class Estadocuota(Serializable, Base):
    way = {}

    __tablename__ = 'estadoCuota'

    id = Column( Integer, primary_key=True)
    nombre = Column(  String(100), nullable=False)

    enabled = Column(Boolean, default=True)







