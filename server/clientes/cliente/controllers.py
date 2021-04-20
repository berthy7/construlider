from .managers import *
from server.common.controllers import CrudController
from server.usuarios.usuario.managers import *

import json


class ClienteController(CrudController):

    manager = ClienteManager
    html_index = "clientes/cliente/views/index.html"

    routes = {
        '/cliente': {'GET': 'index', 'POST': 'table'},
        '/cliente_insert': {'POST': 'insert'},
        '/cliente_update': {'PUT': 'edit', 'POST': 'update'},
        '/cliente_delete': {'POST': 'delete'}
    }

    # def index(self):
    #     print('Entró a index cliente')
    #     self.set_session()
    #     self.verif_privileges()
    #     usuario = self.get_user()
    #     result = self.manager(self.db).listar_todo()
    #     # ob = result['objects']
    #     # print(ob.__dict__)
    #     result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
    #     result.update(self.get_extra_data())
    #     self.render(self.html_index, **result)
    #     self.db.close()


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ClienteManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ClienteManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = ClienteManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
