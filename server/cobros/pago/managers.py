from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from server.ventas.credito.models import *
from server.ventas.contrato.models import *
from server.ventas.cuota.managers import *
from .models import *
from sqlalchemy.sql import func,or_,and_
import decimal


class PagoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Pago, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def listar_pagos_dia(self):

        lista = list()

        fecha = datetime.now(pytz.timezone('America/La_Paz'))
        fechahoy = str(fecha.day)+"/"+str(fecha.month)+"/"+str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        x = self.db.query(self.entity).filter(self.entity.enabled == True).all()

        for i in self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.enabled == True).all():

            idCredito = i.cuota.fkcredito

            objContrato = self.db.query(Contrato).filter(Contrato.fkcredito == idCredito).first()

            cliente = objContrato.reserva.cliente.fullname


            lista.append(dict(id=i.id,fecha=i.fecha.strftime('%d/%m/%Y'),cliente=cliente,fkcredito=idCredito,numeroCuota=i.cuota.numero,monto=i.monto,moneda=i.moneda.codigo,enabled=i.enabled))


        # return self.db.query(self.entity).filter(self.entity.estado == True).filter(self.entity.fechar.cast(Date) == fechahoy).filter(
        #     self.entity.tipo == "Vehicular").all()

        return lista



    def insert(self, dictionary):
        fecha = BitacoraManager(self.db).fecha_actual()
        dictionary['fecha'] = fecha

        if decimal.Decimal(dictionary['monto']) >= decimal.Decimal(dictionary['montoCuotaParcial']):
            cuota = CuotaManager(self.db).cambiar_estado(dictionary['fkcuota'], 'Pagada')

            listaCuotas = CuotaManager(self.db).listar_estado_pendiente_x_credito(cuota.fkcredito)

            if len(listaCuotas) == 0:
                 CreditoManager(self.db).cambiar_estado(cuota.fkcredito, 'Concluido')


        objeto = PagoManager(self.db).entity(**dictionary)

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pago.", fecha=fecha, tabla="pago",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = PagoManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pago.", fecha=fecha,tabla="pago", identificador=a.id)
        super().insert(b)

        return a


    def delete(self, id, Usuario, ip, enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó Pago."
        else:
            mensaje = "Se deshabilitó Pago."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="pago", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


    def obtener_cuota_x_pagar(self, idCredito):
        cuotas = self.db.query(Cuota).join(Estadocuota).filter(Cuota.fkcredito == idCredito).filter(Estadocuota.nombre != "Pagada").order_by(Cuota.numero.asc())

        dicc = ""

        for c in cuotas:
            montoPago = self.db.query(func.sum(Pago.monto)).filter(Pago.fkcuota == c.id).scalar()

            if montoPago:

                montoCuotaParcial = c.monto - montoPago
            else:
                montoCuotaParcial = c.monto

            montoCuotaParcial_format = "{:.2f}".format(montoCuotaParcial)


            dicc = dict(idCuota=c.id,numeroCuota=c.numero,montoCuota=c.monto,montoCuotaParcial=montoCuotaParcial_format,fechaVencimiento=c.fechaVencimiento.strftime('%d/%m/%Y'),estadoCuota=c.estadocuota.nombre,moneda=c.moneda.codigo)
            break


        return dicc


class TipopagoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Tipopago, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def obtener_x_nombre(self,nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(self.entity.enabled == True).first()

