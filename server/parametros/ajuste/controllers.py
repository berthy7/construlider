from .managers import *
from server.common.controllers import CrudController
from server.parametros.moneda.controllers import *

import json


class AjusteController(CrudController):

    manager = AjusteManager
    html_index = "parametros/ajuste/views/index.html"

    routes = {
        '/ajuste': {'GET': 'index', 'POST': 'table'},
        '/ajuste_insert': {'POST': 'insert'},
        '/ajuste_update': {'PUT': 'edit', 'POST': 'update'},
        '/ajuste_delete': {'POST': 'delete'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['monedas'] = MonedaManager(self.db).listar_todo()
        aux['ajuste'] = AjusteManager(self.db).obtener()

        return aux


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        AjusteManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        dictionary['id'] = 1
        AjusteManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')

