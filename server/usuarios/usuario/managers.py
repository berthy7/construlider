from ...operaciones.bitacora.managers import *
from ..rol.models import *

from server.common.managers import SuperManager, Error
from .models import *
from sqlalchemy.sql import func
from random import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xhtml2pdf import pisa

import string
from random import *
import random
import requests
import jwt
import time
import hashlib
import json
from configparser import ConfigParser

class UsuarioManager(SuperManager):

    def __init__(self, db):
        super().__init__(Usuario, db)

    def obtener_administrador(self):
        return self.db.query(Usuario).filter(Usuario.nombre == "Administrador").one()


    def insert(self, dictionary):

        dictionary['password']= hashlib.sha512(dictionary['password'].encode()).hexdigest()

        usuario = UsuarioManager(self.db).entity(**dictionary)
        # user = self.db.query(Usuario).filter(Usuario.username == usuario.username).first()


        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().update(usuario)
        b = Bitacora(fkusuario=usuario.user_id, ip=usuario.ip, accion="Se registró un usuario.", fecha=fecha)
        super().insert(b)

        return a


    def update(self, usuario):

        if not usuario.password or usuario.password == '':
            usuario.password = (self.db.query(Usuario.password)
                .filter(Usuario.id == usuario.id).first())[0]
        else:
            usuario.password = hashlib.sha512(usuario.password.encode()).hexdigest()

        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().update(usuario)
        b = Bitacora(fkusuario=usuario.user_id, ip=usuario.ip, accion="Modificó Usuario.", fecha=fecha, tabla="usuario", identificador=a.id)
        super().insert(b)

        return a



    def delete_user(self, id, enable, Usuariocr, ip):
        x = self.db.query(Usuario).filter(Usuario.id == id).one()

        if enable == True:
            r = self.db.query(Rol).filter(Rol.id == x.fkrol).one()
            if r.enabled:
                x.enabled = enable
            else:
                return False
            message = "Se habilitó un usuario."
        else:
            x.enabled = enable
            message = "Se deshabilitó un usuario."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuariocr, ip=ip, accion=message, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return True

    def get_privileges(self, id, route):
        parent_module = self.db.query(Modulo).join(Rol.modulos).join(Usuario).            \
            filter(Modulo.route == route).\
            filter(Usuario.id == id).\
            filter(Usuario.enabled).\
            first()
        if not parent_module:
            return dict()
        modules = self.db.query(Modulo).\
            join(Rol.modulos).join(Usuario).\
            filter(Modulo.fkmodulo == parent_module.id).\
            filter(Usuario.id == id).\
            filter(Usuario.enabled)
        privileges = {parent_module.name: parent_module}
        for module in modules:
            privileges[module.name] = module
        return privileges

    def list_all(self):
        return dict(objects=self.db.query(Usuario).filter(Usuario.fkrol == Rol.id).filter(Rol.nombre != "ADMINISTRADOR").distinct())

    def has_access(self, id, route):
        aux = self.db.query(Usuario.id).\
            join(Rol).join(Acceso).join(Modulo).\
            filter(Usuario.id == id).\
            filter(Modulo.route == route).\
            filter(Usuario.enabled).\
            all()
        return len(aux) != 0

    def get_page(self, page_nr=1, max_entries=10, like_search=None, order_by=None, ascendant=True, query=None):
        query = self.db.query(Usuario).join(Rol).filter(Rol.id > 1)
        return super().get_page(page_nr, max_entries, like_search, order_by, ascendant, query)

    def login_Usuario(self, username, password):
        password = hashlib.sha512(password.encode()).hexdigest()
        return self.db.query(Usuario).filter(Usuario.username == username).filter(Usuario.password == password).filter(
            Usuario.enabled == 1)

    def get_userById(self, id):
        return dict(profile=self.db.query(Usuario).filter(Usuario.id == id).first())

    def obtener_diccionario_usuario(self, id):
        usuario = self.db.query(Usuario).filter(Usuario.id == id).first()


        return dict(id=usuario.id, username=usuario.username,rol=usuario.rol.nombre,nombre = usuario.fullname)

    def update_password(self, Usuario):
        Usuario.password = hashlib.sha512(Usuario.password.encode()).hexdigest()
        return super().update(Usuario)



    def get_by_password(self, Usuario_id, password):
        return self.db.query(Usuario).filter(Usuario.id == Usuario_id). \
            filter(Usuario.password == hashlib.sha512(str(password).encode()).hexdigest()).first()

    def get_by_pass(self, Usuario_id):
        return self.db.query(Usuario).filter(Usuario.id == Usuario_id).first()

    def obtener_x_codigo(self, codigo):
        return self.db.query(Usuario).filter(Usuario.codigo == codigo).first()


    def listar_todo(self):
        return self.db.query(Usuario).filter(Usuario.enabled == True).filter(Usuario.id != 1).all()

    def update_profile(self, Usuarioprf):
        usuario = self.db.query(Usuario).filter_by(id=Usuarioprf['id']).first()

        existe_usuario = self.db.query(Usuario).filter(Usuario.username == Usuarioprf['username']).first()
        if existe_usuario is None:

            usuario.username = Usuarioprf['username']
            self.db.merge(usuario)
            b = Bitacora(fkusuario=usuario.id, ip=Usuarioprf['ip'], accion="Se actualizó perfil de usuario.", fecha=fecha_zona, tabla='usuario', identificador=usuario.id)
            super().insert(b)
            self.db.commit()

            return True

        else:
            return False



    def verificar_username(self, username):
        n = self.db.query(func.count(Usuario.id)).filter(Usuario.username == username).scalar()

        if n > 0:
            return dict(respuesta=True)

        else:
            return dict(respuesta=False)


    def actualizar_credenciales(self, dictionary):
        usuario = UsuarioManager(self.db).get_by_pass(dictionary['user'])
        old_password = hashlib.sha512(dictionary['password'].encode()).hexdigest()
        if usuario.password == old_password:
            usuario.password = dictionary['nuevo_password']
            if not usuario.password or usuario.password == '':
                usuario.password = (self.db.query(Usuario.password)
                                    .filter(Usuario.id == usuario.id).first())[0]
            else:
                usuario.password = hashlib.sha512(usuario.password.encode()).hexdigest()

            if dictionary['username'] or dictionary['username'] != '':
                usuario.username = dictionary['username']


            fecha = BitacoraManager(self.db).fecha_actual()
            us = self.db.merge(usuario)
            self.db.commit()

            b = Bitacora(fkusuario=dictionary['user'], ip=dictionary['ip'], accion="Modificó Credenciales", fecha=fecha,
                         tabla="usuario", identificador=usuario.id)
            super().insert(b)

            principal = self.db.query(Principal).first()

            if principal.estado == False:

                url = "http://sistemacondominio.herokuapp.com/api/v1/actualizar_credenciales"

                headers = {'Content-Type': 'application/json'}
                dictionary['user'] = us.codigo
                cadena = json.dumps(dictionary)
                body = cadena
                resp = requests.post(url, data=body, headers=headers, verify=False)
                response = json.loads(resp.text)

            return dict(response=None,success=True,message="Actualizado Correctamente")
        else:
            return dict(response=None,success=False,message="Password Incorrecto")


    def restablecer_password(self, dictionary):

        usuario = UsuarioManager(self.db).get_by_pass(dictionary['idusuario'])

        nuevo_password = hashlib.sha512(dictionary['password'].encode()).hexdigest()

        usuario.password = nuevo_password


        fecha = BitacoraManager(self.db).fecha_actual()
        u = super().update(usuario)

        b = Bitacora(fkusuario=dictionary['user'], ip=dictionary['ip'], accion="Restablecio Password", fecha=fecha,
                     tabla="usuario", identificador=usuario.id)
        super().insert(b)

        UsuarioManager(self.db).correo_password_reinicio(u, dictionary['password'])

        return dict(response=None, success=True, message="Actualizado Correctamente")


class ModuloManager:

    def __init__(self, db):
        self.db = db

    def list_all(self):
        return self.db.query(Modulo).filter(Modulo.fkmodulo==None)
