from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from ...database.models import Base
from server.database.serializable import Serializable



class Moneda(Serializable, Base):
    way = {'tipoCambio': {}}

    __tablename__ = 'moneda'

    id = Column( Integer, primary_key=True)
    codigo = Column( String(50), nullable=False)
    nombre = Column( String(200), nullable=False)
    cambio = Column(Float, nullable=True)
    fktipoCambio = Column(Integer, ForeignKey('moneda.id'), nullable=True)

    enabled = Column(Boolean, default=True)
    tipoCambio = relationship('Moneda')
