from sqlalchemy import Column, Integer, String, Boolean, Sequence,Text
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable
from sqlalchemy.ext.hybrid import hybrid_property


class Usuario(Serializable, Base):
    way = {'rol': {'modulos': {}}}

    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=True, default='')
    apellidos = Column(String(250), nullable=True, default='')
    telefono = Column(String(100), nullable=True, default='')
    correo = Column(String(255), nullable=True)
    carnet = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    token = Column(Text, nullable=True, default='Sin Token')
    fkrol = Column(Integer, ForeignKey('rol.id'), nullable=False)
    enabled = Column(Boolean, default=True)

    rol = relationship('Rol')


    def get_dict(self, way=None):
        dictionary = super().get_dict(way)

        dictionary['fullname'] = str(self.nombre)  + " " + str(self.apellidos)
        del(dictionary['password'])
        return dictionary


    @hybrid_property
    def fullname(self):
        aux = ""
        if self.apellidos is not None:
            aux = self.apellidos + " "
        else:
            aux = " "

        if self.nombre is not None:
            aux += self.nombre
        else:
            aux = " "

        return aux


Acceso = Table('acceso', Base.metadata,
               Column('id', Integer, primary_key=True),
               Column('fkrol', Integer, ForeignKey('rol.id')),
               Column('fkmodulo', Integer, ForeignKey('modulo.id')))


class Modulo(Serializable, Base):
    way = {'roles': {}, 'children': {}}

    __tablename__ = 'modulo'

    id = Column(Integer,  primary_key=True)
    route = Column(String(100))
    title = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    icon = Column(String(50), nullable=False, default='home')
    menu = Column(Boolean, nullable=False, default=True)
    fkmodulo = Column(Integer, ForeignKey('modulo.id'))

    roles = relationship('Rol', secondary=Acceso)
    children = relationship('Modulo')


class ServidorCorreo(Serializable, Base):
    way = {}

    __tablename__ = 'servidorCorreo'

    id = Column(Integer, primary_key=True)
    servidor = Column(String(200), nullable=False)
    puerto = Column(String(100), nullable=False)
    correo = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    estado = Column(Boolean, default=True)


class Principal(Serializable, Base):
    way = {}

    __tablename__ = 'principal'

    id = Column(Integer, primary_key=True)
    estado = Column(Boolean, default=False)
