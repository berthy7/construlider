from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable



class Reserva(Serializable, Base):
    way = {}

    __tablename__ = 'reserva'

    id = Column( Integer, primary_key=True)
    fecha = Column( DateTime, nullable=False)
    monto = Column( Float, nullable=False)


    enabled = Column(Boolean, default=True)




