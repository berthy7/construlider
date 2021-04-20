from .managers import *
from server.common.controllers import CrudController

import json


class MonedaController(CrudController):

    manager = MonedaManager
    html_index = "parametros/moneda/views/index.html"

    routes = {
        '/moneda': {'GET': 'index', 'POST': 'table'},
        '/moneda_insert': {'POST': 'insert'},
        '/moneda_update': {'PUT': 'edit', 'POST': 'update'},
        '/moneda_delete': {'POST': 'delete'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['monedas'] = MonedaManager(self.db).listar_todo()

        return aux



    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        MonedaManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        MonedaManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')

