from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable


class Entidad(Serializable, Base):
    way = {}

    __tablename__ = 'entidad'

    id = Column( Integer, primary_key=True)
    nombre = Column( String(50), nullable=False)


    enabled = Column(Boolean, default=True)

