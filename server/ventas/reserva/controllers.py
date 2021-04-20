from .managers import *
from server.common.controllers import CrudController
from server.clientes.cliente.managers import *
from server.terrenos.urbanizacion.managers import *
from server.terrenos.terreno.managers import *
from server.parametros.moneda.managers import *
from server.parametros.ajuste.managers import *
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

class ReservaController(CrudController):

    manager = ReservaManager
    html_index = "ventas/reserva/views/index.html"

    routes = {
        '/reserva': {'GET': 'index', 'POST': 'table'},
        '/reserva_insert': {'POST': 'insert'},
        '/reserva_update': {'PUT': 'edit', 'POST': 'update'},
        '/reserva_delete': {'POST': 'delete'},
        '/reserva_cancel': {'PUT': 'edit', 'POST': 'cancel'},
        '/reserva_reporte_xls': {'POST': 'reporte_xls'},
        '/reserva_reporte_pdf': {'POST': 'reporte_pdf'},
        '/reserva_listar_para_contrato': {'POST': 'listar_para_contrato'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        aux['clientes'] = ClienteManager(self.db).listar_todo()
        aux['urbanizaciones'] = UrbanizacionManager(self.db).listar_habilitados()
        aux['tipoterrenos'] = TipoterrenoManager(self.db).listar_todo()
        aux['terrenos'] = TerrenoManager(self.db).listar_todo()
        aux['monedas'] = MonedaManager(self.db).listar_todo()
        aux['ajuste'] = AjusteManager(self.db).obtener()

        return aux


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ReservaManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        ReservaManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = ReservaManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()

    def cancel(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        ReservaManager(self.db).cancel(dictionary['id'], self.get_user_id(), self.request.remote_ip)
        self.respond(success=True, message='Cancelado correctamente.')

    def reporte_xls(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        cname = self.manager(self.db).reporte_excel(dictionary['id'])
        self.respond({'nombre': cname, 'url': 'resources/downloads/' + cname}, True)
        self.db.close()

    def reporte_pdf(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        detalle = ""
        logoempresa = "/resources/images/sinImagen.jpg"

        x = self.db.query(Reserva).filter(Reserva.id ==dictionary['id']).first()

        html = "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
               "<style>" \
               "   .border-own { border-left: 0px; border-right: 0px; }" \
               "   .border-own-l { border-right: 0px; }" \
               "   .border-own-r { border-left: 0px; }" \
               "   @page {size: letter portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
               "</style>" \
               "<div class='container' style='font-size: 12px'>" \
               "   <div class='row'>" \
               "       <div class='col-md-4'>" \
               "           <img src='../server/common" + logoempresa + "' width='auto' height='75'>" \
               "       </div>" \
               "   </div>" \
               "</div>"

        html += "" \
                "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "<tr color='#ffffff' >" \
                "   <th colspan='22' scope='colgroup' align='left' style='background-color: #1976d2; font-size=4; color: white; margin-top: 4px'>BOLETA DEVOLUCION #" + str(x.id) + "</th>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; border-top:1px solid grey; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Cliente: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.cliente.fullname) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px;'>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Fecha Reserva: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.fechaReserva.strftime('%d/%m/%Y')) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Urbanizacion: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.terreno.manzano.urbanizacion.direccion) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px;'>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Manzano: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.terreno.manzano.calle1) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px;'>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Tipo: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.terreno.tipoterreno.nombre) + "</font></td>" \
                "</tr>"\
                "<tr style='font-size: 12px; border: 0px;'>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Terreno: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>Codigo Terreno</font></td>" \
                "</tr>"\
                "<tr style='font-size: 12px; border: 0px;'>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Monto: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.monto) + "</font></td>" \
                "</tr>" \
                 "<tr style='font-size: 12px; border: 0px;'>" \
                 "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Estado: </strong></td>" \
                 "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.estadoreserva.nombre) + "</font></td>" \
                 "</tr>" \
                 "<tr style='font-size: 12px; border: 0px;'>" \
                 "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Fecha Devolucion: </strong></td>" \
                 "   <td colspan='17' scope='colgroup'align='left'><font>" + str(x.fechaDevolucion.strftime('%d/%m/%Y')) + "</font></td>" \
                 "</tr>" \
                   "<tr style='font-size: 12px; border: 0px;'>" \
                   "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'></td>" \
                   "   <td colspan='17' scope='colgroup'align='left'></td>" \
                  "</tr>"\
                "<tr style='font-size: 12px; border: 0px;'>" \
                 "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'></td>" \
                 "   <td colspan='17' scope='colgroup'align='left'></td>" \
                 "</tr>" \
                    "<tr style='font-size: 12px; border: 0px;'>" \
                 "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Firma Cliente: </strong></td>" \
                 "   <td colspan='17' scope='colgroup'align='left'><font>.....................</font></td>" \
                 "</tr>" \
               "</tr>" \
               "<tr style='font-size: 12px; border: 0px;'>" \
               "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'></td>" \
               "   <td colspan='17' scope='colgroup'align='left'></td>" \
               "</tr>" \
               "</table>" \
                 "</br>"

        nombre = "Reporte_devolucion.pdf"

        report.html_to_pdf(html, nombre)
        self.respond('/resources/downloads/' + nombre)

    def listar_para_contrato(self):
        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = ReservaManager(self.db).listar_para_contrato(data['idreserva'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()