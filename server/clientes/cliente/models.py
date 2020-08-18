from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Cliente(Serializable, Base):
    way = {}

    __tablename__ = 'cliente'

    id = Column( Integer, primary_key=True)
    nombre = Column( String(50), nullable=False)
    apellidos = Column( String(200), nullable=False)
    carnet = Column(String(100), nullable=False)
    telefono = Column(String(100), nullable=True)

    enabled = Column(Boolean, default=True)

