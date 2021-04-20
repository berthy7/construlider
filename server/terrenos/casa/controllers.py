from .managers import *
from server.common.controllers import CrudController
from server.terrenos.urbanizacion.managers import *
from server.parametros.moneda.managers import *
import os.path
import uuid

import json


class CasaController(CrudController):

    manager = CasaManager
    html_index = "terrenos/casa/views/index.html"
    routes = {
        '/casa': {'GET': 'index', 'POST': 'table'},
        '/casa_insert': {'POST': 'insert'},
        '/casa_update': {'PUT': 'edit', 'POST': 'update'},
        '/casa_delete': {'POST': 'delete'},
        '/casa_verificar': {'POST': 'verificar'}
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

        CasaManager(self.db).insert(dictionary)
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
        CasaManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = CasaManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()


    def verificar(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        idurbanizacion = dictionary['idurbanizacion']
        repetido = CasaManager(self.db).verificar(idurbanizacion)
        self.respond(success=repetido['respuesta'])

