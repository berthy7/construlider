from .managers import *
from server.common.controllers import CrudController

import json


class ReporteController(CrudController):

    manager = ReporteManager
    html_index = "flujo/reporte/views/index.html"

    routes = {
        '/reporte': {'GET': 'index', 'POST': 'table'},
        '/reporte_insert': {'POST': 'insert'},
        '/reporte_update': {'PUT': 'edit', 'POST': 'update'},
        '/reporte_delete': {'POST': 'delete'}
    }


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ReporteManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ReporteManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')

