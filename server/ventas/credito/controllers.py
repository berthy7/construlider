from .managers import *
from server.common.controllers import CrudController
# from server.terrenos.urbanizacion.managers import *

import json


class CreditoController(CrudController):

    manager = CreditoManager
    html_index = "ventas/credito/views/index.html"
    html_table = "ventas/credito/views/table.html"
    routes = {
        '/credito': {'GET': 'index', 'POST': 'table'},
        '/credito_insert': {'POST': 'insert'},
        '/credito_update': {'PUT': 'edit', 'POST': 'update'},
        '/credito_delete': {'POST': 'delete'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        # aux['urbanizaciones'] = UrbanizacionManager(self.db).listar_habilitados()

        return aux


    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        CreditoManager(self.db).insert(diccionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        CreditoManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = CreditoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
