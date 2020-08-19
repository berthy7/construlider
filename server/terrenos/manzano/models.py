from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Manzano(Serializable, Base):
    way = {'contrato': {}}

    __tablename__ = 'manzano'

    id = Column( Integer, primary_key=True)
    numero = Column( String(50), nullable=False)
    calle1 = Column( String(100), nullable=False)
    calle2 = Column(String(100), nullable=False)
    fkurbanizacion = Column(Integer, ForeignKey('urbanizacion.id'), nullable=True)

    enabled = Column(Boolean, default=True)

    urbanizacion = relationship('Urbanizacion')


