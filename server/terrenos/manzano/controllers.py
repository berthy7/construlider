from .managers import *
from server.common.controllers import CrudController
from server.terrenos.urbanizacion.managers import *

import json


class ManzanoController(CrudController):

    manager = ManzanoManager
    html_index = "terrenos/manzano/views/index.html"

    routes = {
        '/manzano': {'GET': 'index', 'POST': 'table'},
        '/manzano_insert': {'POST': 'insert'},
        '/manzano_update': {'PUT': 'edit', 'POST': 'update'},
        '/manzano_delete': {'POST': 'delete'},
        '/manzano_listar_x_urbanizacion': {'POST': 'listar_x_urbanizacion'},
    }



    def get_extra_data(self):
        aux = super().get_extra_data()

        aux['urbanizaciones'] = UrbanizacionManager(self.db).listar_habilitados()

        return aux


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ManzanoManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ManzanoManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = ManzanoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()


    def listar_x_urbanizacion(self):
        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = ManzanoManager(self.db).listar_x_urbanizacion(data['idurbanizacion'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()