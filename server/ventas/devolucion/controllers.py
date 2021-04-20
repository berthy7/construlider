from .managers import *
from server.common.controllers import CrudController
from server.clientes.cliente.managers import *
from server.terrenos.urbanizacion.managers import *
from server.terrenos.terreno.managers import *
from xhtml2pdf import pisa

import os.path
import uuid
import json


class Report:
    def html_to_pdf(self, sourceHtml, nombre):
        outputFilename = 'server/common/resources/downloads/' + nombre

        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(
            sourceHtml,
            dest=resultFile)
        resultFile.close()

        return pisaStatus.err

global report
report = Report()

class DevolucionController(CrudController):

    manager = DevolucionManager
    html_index = "ventas/devolucion/views/index.html"

    routes = {
        '/devolucion': {'GET': 'index', 'POST': 'table'},
        '/devolucion_insert': {'POST': 'insert'},
        '/devolucion_update': {'PUT': 'edit', 'POST': 'update'},
        '/devolucion_delete': {'POST': 'delete'},
        '/devolucion_cancel': {'PUT': 'edit', 'POST': 'cancel'},
        '/devolucion_reporte_xls': {'POST': 'reporte_xls'},
        '/devolucion_reporte_pdf': {'POST': 'reporte_pdf'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        aux['clientes'] = ClienteManager(self.db).listar_todo()
        aux['urbanizaciones'] = UrbanizacionManager(self.db).listar_habilitados()
        aux['tipoterrenos'] = TipoterrenoManager(self.db).listar_todo()
        aux['terrenos'] = TerrenoManager(self.db).listar_todo()

        return aux


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        DevolucionManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        DevolucionManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = DevolucionManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()

    def cancel(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        DevolucionManager(self.db).cancel(dictionary['id'], self.get_user_id(), self.request.remote_ip)
        self.respond(success=True, message='Cancelado correctamente.')


    def reporte_xls(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        cname = self.manager(self.db).reporte_excel()
        self.respond({'nombre': cname, 'url': 'resources/downloads/' + cname}, True)
        self.db.close()

    def reporte_pdf(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        detalle = ""


        html = "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
               "<style>" \
               "   .border-own { border-left: 0px; border-right: 0px; }" \
               "   .border-own-l { border-right: 0px; }" \
               "   .border-own-r { border-left: 0px; }" \
               "   @page {size: letter landscape; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
               "</style>" \
               "<div class='container' style='font-size: 12px'>" \
               "   <div class='row'>" \
               "       <div class='col-md-4'>" \
                "       </div>" \
                "   </div>" \
                "   <div class='row'>" \
                "       <div class='col-md-4'>" \
                "           <h6 align='center'>ANALISIS DE PROCEDIMIENTOS</h6>" \
                "       </div>" \
                "   </div>" \
                "</div>"

        html += "<table align='center' style='padding: 4px; border: 1px solid white' width='100%'>" \
                "   <tr style='font-size: 12px'>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Fecha</th>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Procedimiento</th>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Relator</th>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Cantidad de Participantes</th>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Cantidad de No Participantes</th>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Empresa</th>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Gerencia</th>" \
                "       <th colspan='2' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>GPR</th>" \
                "   </tr>" \
                "" + detalle + "" \
                               "</table>"

        nombre = "Reporte_devolucion.pdf"

        report.html_to_pdf(html, nombre)
        self.respond('/resources/downloads/' + nombre)