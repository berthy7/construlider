from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable



class Credito(Serializable, Base):
    way = {'estadocredito': {},'entidad': {}}

    __tablename__ = 'credito'

    id = Column( Integer, primary_key=True)
    numeroCuotas = Column( Integer, nullable=False)
    capital = Column( Float, nullable=False)
    fkentidad = Column(Integer, ForeignKey('entidad.id'), nullable=True)
    fkestadocredito = Column(Integer, ForeignKey('estadoCredito.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    estadocredito = relationship('Estadocredito')
    entidad = relationship('Entidad')


class Estadocredito(Serializable, Base):
    way = {}

    __tablename__ = 'estadoCredito'

    id = Column( Integer, primary_key=True)
    nombre = Column(  String(100), nullable=False)

    enabled = Column(Boolean, default=True)


class Cuota(Serializable, Base):
    way = {'credito': {},'estadocuota': {}}

    __tablename__ = 'cuota'

    id = Column( Integer, primary_key=True)
    monto = Column( Float, nullable=False)
    fechaVencimiento = Column( Float, nullable=False)
    fkcredito = Column(Integer, ForeignKey('credito.id'), nullable=True)
    fkestadocuota = Column(Integer, ForeignKey('estadoCuota.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    credito = relationship('Credito')
    estadocuota = relationship('Estadocuota')



class Estadocuota(Serializable, Base):
    way = {}

    __tablename__ = 'estadoCuota'

    id = Column( Integer, primary_key=True)
    nombre = Column(  String(100), nullable=False)

    enabled = Column(Boolean, default=True)


