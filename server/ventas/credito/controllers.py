from .managers import *
from server.common.controllers import CrudController
from server.ventas.entidad.managers import *

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
        '/credito_delete': {'POST': 'delete'},
        '/credito_listar_x_cliente': {'POST': 'listar_x_cliente'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['entidades'] = EntidadManager(self.db).listar_todo()
        aux['estadocreditos'] = EstadocreditoManager(self.db).listar_todo()
        aux['creditos'] = CreditoManager(self.db).listar_diccionario()

        return aux


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        CreditoManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')


    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        CreditoManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = CreditoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()


    def listar_x_cliente(self):
        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = CreditoManager(self.db).listar_x_cliente(data['idcliente'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()
