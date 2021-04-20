from .managers import *
from server.common.controllers import CrudController
from server.ventas.reserva.managers import *
from server.ventas.entidad.managers import *
from server.ventas.credito.managers import *

import json


class ContratoController(CrudController):

    manager = ContratoManager
    html_index = "ventas/contrato/views/index.html"
    html_table = "ventas/contrato/views/table.html"
    routes = {
        '/contrato': {'GET': 'index', 'POST': 'table'},
        '/contrato_insert': {'POST': 'insert'},
        '/contrato_update': {'PUT': 'edit', 'POST': 'update'},
        '/contrato_delete': {'POST': 'delete'},
        '/contrato_obtener_reserva': {'PUT': 'obtener_reserva'},
        '/contrato_valor_cuota': {'PUT': 'valor_cuota'}



    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        aux['reservas'] = ReservaManager(self.db).listar_todo()
        aux['tipoventas'] = TipoventaManager(self.db).listar_todo()
        aux['entidades'] = EntidadManager(self.db).listar_todo()

        return aux


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        objeto_credito = CreditoManager(self.db).insert(dictionary)

        dictionary['fkcredito'] = objeto_credito.id
        dictionary['monto'] = objeto_credito.capital

        ContratoManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')


    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        objeto_credito = CreditoManager(self.db).update(dictionary)

        dictionary['fkcredito'] = objeto_credito.id
        dictionary['monto'] = objeto_credito.capital

        ContratoManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = ContratoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()


    def obtener_reserva(self):
        self.set_session()
        # self.verif_privileges()
        ins_manager = self.manager(self.db)
        dictionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtener_reserva(dictionary['id'])

        self.respond(indicted_object, message='Operacion exitosa!')
        self.db.close()


    def valor_cuota(self):
        self.set_session()
        # self.verif_privileges()
        ins_manager = self.manager(self.db)
        dictionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.valor_cuota(dictionary['valorCredito'],dictionary['numeroCuotas'],
                                                  dictionary['montoReserva'],dictionary['cuotaInicial'],
                                                  dictionary['fechaPrimerCuota'])

        self.respond(indicted_object, message='Operacion exitosa!')
        self.db.close()
