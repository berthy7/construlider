from tornado.gen import coroutine
from .managers import *
from ...common.controllers import CrudController, SuperController, ApiController
from ..rol.managers import *
import json

from server.database.connection import transaction


class UsuarioController(CrudController):
    manager = UsuarioManager
    html_index = "usuarios/usuario/views/index.html"
    html_table = "usuarios/usuario/views/table.html"
    routes = {
        '/usuario': {'GET': 'index', 'POST': 'table'},
        '/usuario_insert': {'POST': 'insert'},
        '/usuario_update': {'PUT': 'edit', 'POST': 'update'},
        '/usuario_delete': {'POST': 'delete_user'},
        '/usuario_activate': {'POST': 'activate_user'},
        '/usuario_profile': {'GET': 'usuario_profile'},
        '/usuario_update_profile': {'POST': 'user_update_profile'},
        '/usuario_update_password': {'POST': 'user_update_password'},
        '/usuario_reset_password': {'POST': 'usuario_reset_password'},

        '/usuario_verificar_username': {'POST': 'verificar_username'},
        '/usuario_restablecer_password': {'POST': 'restablecer_password'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()

        aux['roles'] = RolManager(self.db).listar_todo()
        aux['usuarios'] = UsuarioManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        us = self.get_user()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user_id'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        diccionary['username'] = diccionary['correo']
        diccionary['password'] = diccionary['ci']

        respuesta = UsuarioManager(self.db).insert(diccionary)


    def update(self):
        self.set_session()
        us = self.get_user()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user_id'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        UsuarioManager(self.db).update(objeto)


    def delete_user(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        enable = diccionary['enabled']
        resp = UsuarioManager(self.db).delete_user(id, enable, self.get_user_id(), self.request.remote_ip)

        if resp:
            if enable == True:
                msg = 'Usuario activado correctamente.'
            else:
                msg = 'Usuario eliminado correctamente.'
            self.respond(success=True, message=msg)
        else:
            msg = 'Perfil asignado deshabilitado, no es posible habilitar el usuario.'
            self.respond(success=False, message=msg)

    def activate_user(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        UsuarioManager(self.db).activate_users(id, self.get_user_id(), self.request.remote_ip)
        self.respond(success=True, message='Usuario activado correctamente.')

    def usuario_profile(self):
        user = self.get_user()
        self.set_session()
        usuario = UsuarioManager(self.db)
        result = usuario.obtener_diccionario_usuario(self.get_user_id())
        self.render("usuarios/usuario/views/profile.html", user=user, **result)
        self.db.close()

    def user_update_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        user = self.manager(self.db).get_by_password(self.get_user_id(), diccionary['old_password'])
        if user:
            if diccionary['new_password'] == diccionary['new_password_2']:
                user.password = diccionary['new_password']
                self.manager(self.db).update_password(user)
                self.respond(message="Contraseña cambiada correctamente ", success=True)
            else:
                self.respond(message="Datos incorrectos", success=False)
        else:
            self.respond(message="Datos incorrectos", success=False)
        self.db.close()

    def user_reset_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        user = self.manager(self.db).get_by_pass(self.get_user_id())
        if user:
            if diccionary['new_password'] == diccionary['new_password_2']:
                user.password = diccionary['new_password']
                self.manager(self.db).update_password(user)
                self.respond(message="Contraseña cambiada correctamente ", success=True)
            else:
                self.respond(message="Datos incorrectos", success=False)
        else:
            self.respond(message="Datos incorrectos", success=False)
        self.db.close()

    def user_update_profile(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        user = self.manager(self.db).update_profile(objeto, diccionary['ip'])
        self.respond(message="Datos Correctos", success=True)
        self.db.close()

    def usuario_codigo_reset(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        self.manager(self.db).update_codigo(id)
        self.respond(success=True, message='Modificado Correctamente!')

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def obtener_x_condominio(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        arraT = UsuarioManager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = UsuarioManager(self.db).obtener_x_condominio(data['idcondominio'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()

    def verificar_username(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        repetido = UsuarioManager(self.db).verificar_username(username)
        if repetido['respuesta']:
            self.respond(message='', success=False)
        else:
            self.respond(message='', success=True)

    def restablecer_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        resp = UsuarioManager(self.db).restablecer_password(diccionary)
        self.respond(resp)



class ApiUserController(ApiController):
    routes = {
        '/api/v1/login_usuario_mobile': {'POST': 'login_usuario_mobile'},
        '/api/v1/update_token_usuario': {'POST': 'update_token_usuario'},
        '/api/v1/listar_usuarios_privilegios': {'POST': 'listar_usuarios_privilegios'},
        '/api/v1/update_movil_privilegio': {'POST': 'update_movil_privilegio'},
    }

    def check_xsrf_cookie(self):
        return


class ManualController(SuperController):

    @coroutine
    def get(self):
        usuario = self.get_user()
        self.render("usuarios/usuario/views/manual.html",   user=usuario)
