from .managers import *
from server.common.controllers import CrudController
from server.clientes.cliente.managers import *
from server.ventas.entidad.managers import *
from server.cobros.pago.managers import *
from server.parametros.moneda.managers import *

import json

import os.path
import uuid
import json


class PagoController(CrudController):

    manager = PagoManager
    html_index = "cobros/pago/views/index.html"

    routes = {
        '/pago': {'GET': 'index', 'POST': 'table'},
        '/pago_insert': {'POST': 'insert'},
        '/pago_update': {'PUT': 'edit', 'POST': 'update'},
        '/pago_delete': {'POST': 'delete'},
        '/pago_obtener_cuota_x_pagar': {'PUT': 'obtener_cuota_x_pagar'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        aux['clientes'] = ClienteManager(self.db).listar_todo()
        aux['entidades'] = EntidadManager(self.db).listar_todo()
        aux['tipopagos'] = TipopagoManager(self.db).listar_todo()
        aux['lista_pagos'] = PagoManager(self.db).listar_pagos_dia()
        aux['monedas'] = MonedaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/comprobantePago/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['fotoComprobante'] = "/resources/images/comprobantePago/" + cname

        PagoManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/comprobantePago/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['fotoComprobante'] = "/resources/images/comprobantePago/" + cname

        PagoManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = PagoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()


    def obtener_cuota_x_pagar(self):
        self.set_session()
        # self.verif_privileges()
        ins_manager = self.manager(self.db)
        dictionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtener_cuota_x_pagar(dictionary['id'])

        self.respond(indicted_object, message='Operacion exitosa!')
        self.db.close()