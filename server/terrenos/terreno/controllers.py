from .managers import *
from server.common.controllers import CrudController
from server.terrenos.urbanizacion.managers import *
from server.parametros.moneda.managers import *
import os.path
import uuid

import json


class TerrenoController(CrudController):

    manager = TerrenoManager
    html_index = "terrenos/terreno/views/index.html"
    html_table = "terrenos/terreno/views/table.html"
    routes = {
        '/terreno': {'GET': 'index', 'POST': 'table'},
        '/terreno_insert': {'POST': 'insert'},
        '/terreno_update': {'PUT': 'edit', 'POST': 'update'},
        '/terreno_delete': {'POST': 'delete'},
        '/terreno_listar_x_tipo': {'POST': 'listar_x_tipo'},
        '/terreno_verificar': {'POST': 'verificar'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['urbanizaciones'] = UrbanizacionManager(self.db).listar_habilitados()
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
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto1'] = "/resources/images/terrenos/" + cname

        if "archivo2" in self.request.files:
            fileinfo = self.request.files["archivo2"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto2'] = "/resources/images/terrenos/" + cname

        if "archivo3" in self.request.files:
            fileinfo = self.request.files["archivo3"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto3'] = "/resources/images/terrenos/" + cname

        if "archivo4" in self.request.files:
            fileinfo = self.request.files["archivo4"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto4'] = "/resources/images/terrenos/" + cname

        TerrenoManager(self.db).insert(dictionary)
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
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto1'] = "/resources/images/terrenos/" + cname

        if "archivo2" in self.request.files:
            fileinfo = self.request.files["archivo2"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto2'] = "/resources/images/terrenos/" + cname

        if "archivo3" in self.request.files:
            fileinfo = self.request.files["archivo3"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto3'] = "/resources/images/terrenos/" + cname

        if "archivo4" in self.request.files:
            fileinfo = self.request.files["archivo4"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/terrenos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dictionary['foto4'] = "/resources/images/terrenos/" + cname
        TerrenoManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = TerrenoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()

    def listar_x_tipo(self):
        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = TerrenoManager(self.db).listar_x_manzano(data['idmanzano'],data['idtipoterreno'],data['idterreno'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()

    def verificar(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        idurbanizacion = dictionary['idurbanizacion']
        repetido = TerrenoManager(self.db).verificar(idurbanizacion)
        self.respond( success=repetido['respuesta'])

