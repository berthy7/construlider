from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

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
    email = Column(String(100), nullable=False)

    enabled = Column(Boolean, default=True)

    @hybrid_property
    def fullname(self):
        aux = ""
        if self.nombre is not None:
            aux = self.nombre + " "
        else:
            aux = " "

        if self.apellidos is not None:
            aux = aux + self.apellidos + " "
        else:
            aux = " "



        return aux


    def get_dict(self, way=None):
        aux = super().get_dict(way)

        aux['fullname'] = str(self.nombre) + " " + str(self.apellidos)


        return aux

