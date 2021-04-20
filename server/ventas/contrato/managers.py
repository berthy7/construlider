from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from server.ventas.reserva.managers import *
from server.ventas.cuota.models import *
from server.parametros.ajuste.managers import *
from datetime import datetime, timedelta
from .models import *
from sqlalchemy.sql import func,or_,and_
import decimal
from datetime import date


class ContratoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Contrato, db)

    def obtain(self, key):
        x = self.db.query(self.entity).get(key)

        x.credito.cuotas = self.db.query(Cuota).filter(Cuota.fkcredito == x.credito.id).order_by(Cuota.numero.asc()).all()

        return x

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.direccion.asc()).all()

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.direccion.asc()).all()

    def insert(self, dictionary):
        fecha = BitacoraManager(self.db).fecha_actual()
        dictionary['fecha'] = fecha

        dictionary['fechaPrimerCuota'] = datetime.strptime(dictionary['fechaPrimerCuota'], '%d/%m/%Y')

        if dictionary['cuotaInicial'] =="":
            dictionary['cuotaInicial'] = None

        objeto = ContratoManager(self.db).entity(**dictionary)

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Contrato.", fecha=fecha, tabla="contrato",
                     identificador=a.id)
        super().insert(b)

        if a.fkreserva:

            ReservaManager(self.db).venta(a.fkreserva)


        return a

    def update(self, dictionary):
        fecha = BitacoraManager(self.db).fecha_actual()
        dictionary['fecha'] = fecha

        dictionary['fechaPrimerCuota'] = datetime.strptime(dictionary['fechaPrimerCuota'], '%d/%m/%Y')

        if dictionary['cuotaInicial'] =="":
            dictionary['cuotaInicial'] = None

        objeto = ContratoManager(self.db).entity(**dictionary)

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Contrato.", fecha=fecha,tabla="contrato", identificador=a.id)
        super().insert(b)

        return a

    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó Contrato."
        else:
            mensaje = "Se deshabilitó Contrato."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="contrato", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje

    def obtener_reserva(self, idReserva):
        x = self.db.query(Reserva).filter(Reserva.id == idReserva).first()

        valorTerreno = int(x.terreno.superficie) * int(x.terreno.valorMetroCuadrado)

        dicc = x.get_dict()

        dicc['valorTerreno'] = valorTerreno

        ajuste = AjusteManager(self.db).obtener()

        dicc['tasaInteres'] = ajuste.tasaInteres * 100

        interes = valorTerreno * ajuste.tasaInteres

        interes_format = "{:.2f}".format(interes)

        dicc['interes'] = interes_format

        valorCredito = valorTerreno + interes

        dicc['valorCredito'] = valorCredito


        return dicc


    def valor_cuota(self, valorCredito, numeroCuotas, montoReserva, cuotaInicial, fechaPrimerCuota):
        listaCuotas =  list()
        i = 0
        num = 1

        if numeroCuotas != 0:
            valorCuota = valorCredito / numeroCuotas
            for vuelta in range(i, numeroCuotas):

                monto = valorCuota

                if vuelta == 0:
                    if montoReserva and cuotaInicial:
                        monto = valorCuota - montoReserva - cuotaInicial

                    elif montoReserva:
                        monto = valorCuota - montoReserva

                    elif cuotaInicial:
                        monto = valorCuota - cuotaInicial

                    else:
                        monto = valorCuota

                valorMonto_format = "{:.2f}".format(monto)

                listaCuotas.append(dict(numero=str(num),valorCuota=str(valorMonto_format), fechaReserva=str(fechaPrimerCuota)))
                num = num + 1
                try:
                    fecha = datetime.strptime(fechaPrimerCuota, '%d/%m/%Y')
                    carry, new_month = divmod(fecha.month - 1 + 1, 12)
                    new_month += 1
                except Exception as e:
                    carry = 0
                    new_month += 1

                try:

                    current_date = fecha.replace(year=fecha.year + carry, month=new_month)

                    fechaPrimerCuota = current_date.strftime('%d/%m/%Y')
                except Exception as e:
                    fechaPrimerCuota = ''



        else:
            valorCuota = 0
            primervalorCuota = 0


        return listaCuotas


class TipoventaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Tipoventa, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def obtener_x_nombre(self,nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(self.entity.enabled == True).first()



