from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from server.ventas.contrato.models import *
from server.ventas.reserva.models import *
from .models import *
from sqlalchemy.sql import func,or_,and_


class CreditoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Credito, db)

    def list_all(self):

        return dict(objects=self.db.query(self.entity))

    def listar_diccionario(self):
        lista = list()

        for i in self.db.query(self.entity).filter(self.entity.enabled == True).all():

            cont = self.db.query(Contrato).filter(Contrato.fkcredito == i.id).first()




            lista.append(dict(id=i.id,cliente=cont.reserva.cliente.fullname,capital=i.capital,moneda=i.moneda.codigo,numeroCuotas=i.numeroCuotas,entidad=i.entidad.nombre,estadoCredito=i.estadocredito.nombre,enabled=i.enabled))


        return lista


    def obtain(self, key):
        x = self.db.query(self.entity).get(key)
        x.cuotas = self.db.query(Cuota).filter(Cuota.fkcredito == x.id).order_by(Cuota.numero.asc()).all()

        return x

    def cambiar_estado(self,id,estado):

        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        estadocredito = EstadocreditoManager(self.db).obtener_x_nombre(estado)
        x.fkestadocredito = estadocredito.id

        self.db.merge(x)
        self.db.commit()

        return x

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def listar_x_cliente(self, idcliente):

        return self.db.query(Credito).join(Estadocredito).join(Contrato).join(Reserva).filter(Credito.enabled == True).filter(Estadocredito.nombre == "En curso").filter(Reserva.fkcliente == idcliente).all()

    def insert(self, dictionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        fecha_hoy_str = fecha.strftime('%Y-%m-%d %H:%M')
        fechahoy = fecha_hoy_str[0:10]

        fechahoy = datetime.strptime(fechahoy, '%Y-%m-%d')

        for i in dictionary['cuotas']:
            strEstadocuota = "Pendiente"
            i['fechaVencimiento'] = datetime.strptime(i['fechaVencimiento'], '%d/%m/%Y')
            i['fkmoneda'] = dictionary['fkmoneda']

            if fechahoy > i['fechaVencimiento']:
                strEstadocuota = "Mora"



            estadocuota = EstadocuotaManager(self.db).obtener_x_nombre(strEstadocuota)
            i['fkestadocuota']  = estadocuota.id


        estadocredito = EstadocreditoManager(self.db).obtener_x_nombre("En curso")
        dictionary['fkestadocredito'] = estadocredito.id

        objeto = CreditoManager(self.db).entity(**dictionary)


        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Credito.", fecha=fecha, tabla="credito",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        fecha_hoy_str = fecha.strftime('%Y-%m-%d %H:%M')
        fechahoy = fecha_hoy_str[0:10]

        fechahoy = datetime.strptime(fechahoy, '%Y-%m-%d')

        for i in dictionary['cuotas']:
            strEstadocuota = "Pendiente"
            i['fechaVencimiento'] = datetime.strptime(i['fechaVencimiento'], '%d/%m/%Y')
            i['fkmoneda'] = dictionary['fkmoneda']

            if fechahoy > i['fechaVencimiento']:
                strEstadocuota = "Mora"



            estadocuota = EstadocuotaManager(self.db).obtener_x_nombre(strEstadocuota)
            i['fkestadocuota']  = estadocuota.id


        estadocredito = EstadocreditoManager(self.db).obtener_x_nombre("En curso")
        dictionary['fkestadocredito'] = estadocredito.id

        objeto = CreditoManager(self.db).entity(**dictionary)

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Credito.", fecha=fecha,tabla="credito", identificador=a.id)
        super().insert(b)

        return a

    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó reserva."
        else:
            mensaje = "Se deshabilitó reserva."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="credito", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


class EstadocreditoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Estadocredito, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def obtener_x_nombre(self,nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(self.entity.enabled == True).first()


class CuotaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Cuota, db)


    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, dictionary):
        tipoCuota = TipoterrenoManager(self.db).obtener_x_nombre("Cuota")

        dictionary['fktipoterreno'] = tipoCuota.id


        objeto = CuotaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Cuota.", fecha=fecha, tabla="reserva",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = CuotaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Cuota.", fecha=fecha,tabla="reserva", identificador=a.id)
        super().insert(b)

        return a

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


class EstadocuotaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Estadocuota, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def obtener_x_nombre(self,nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(self.entity.enabled == True).first()
