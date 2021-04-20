from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_
from server.terrenos.terreno.managers import *
from datetime import datetime
from openpyxl import Workbook


class ReservaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Reserva, db)


    def listar_para_contrato(self, idreserva):

        x = self.db.query(self.entity).join(Estadoreserva).filter(Estadoreserva.nombre == "Iniciado").filter(self.entity.enabled == True).all()

        if idreserva:

            if self.db.query(self.entity).filter(self.entity.id == idreserva).first():

                x.append(self.db.query(self.entity).filter(self.entity.id == idreserva).first())

        return x



    def list_all(self):
        return dict(objects=self.db.query(self.entity).join(Estadoreserva).filter(Estadoreserva.nombre != "Cancelado"))

    def listar_todo(self):
        return self.db.query(self.entity).join(Estadoreserva).filter(Estadoreserva.nombre == "Iniciado").filter(self.entity.enabled == True).all()

    def insert(self, dictionary):
        TerrenoManager(self.db).cambiar_estado(dictionary['fkterreno'], False)
        dictionary['fechaReserva'] = datetime.strptime(dictionary['fechaReserva'], '%d/%m/%Y')
        dictionary['tipo'] = "Reserva"

        estadoreserva = EstadoreservaManager(self.db).obtener_x_nombre("Iniciado")
        dictionary['fkestadoreserva'] = estadoreserva.id

        objeto = ReservaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Reserva.", fecha=fecha, tabla="reserva",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = ReservaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Reserva.", fecha=fecha,tabla="reserva", identificador=a.id)
        super().insert(b)

        return a

    def cancel(self, id, Usuario, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()
        TerrenoManager(self.db).cambiar_estado(x.fkterreno, True)
        estado = EstadoreservaManager(self.db).obtener_x_nombre("Cancelado")

        fecha = BitacoraManager(self.db).fecha_actual()

        x.fkestadoreserva = estado.id
        x.fechaDevolucion = fecha
        x.tipo = ""

        b = Bitacora(fkusuario=Usuario, ip=ip, accion="Cancelo Reserva", fecha=fecha,tabla="reserva", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return x

    def venta(self, id):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()
        estado = EstadoreservaManager(self.db).obtener_x_nombre("Venta")

        x.fkestadoreserva = estado.id

        self.db.merge(x)
        self.db.commit()

        return x

    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó reserva."
        else:
            mensaje = "Se deshabilitó reserva."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje

    def reporte_excel(self,id):
        fecha = datetime.now()
        cname = "Devolucion_" + fecha.strftime('%Y-%m-%d') + ".xlsx"

        x = self.db.query(Reserva).filter(Reserva.id == id).first()

        wb = Workbook()

        ws = wb.active
        ws.title = 'Boleta Devolucion'

        indice = 0
        # --------------------------------------------------------------------
        indice = indice + 1
        ws['A' + str(indice)] = 'BOLETA DEVOLUCION #' + str(x.id)
        indice = indice + 2


        wb.save("server/common/resources/downloads/" + cname)

        return cname

class EstadoreservaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Estadoreserva, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def obtener_x_nombre(self,nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(self.entity.enabled == True).first()



