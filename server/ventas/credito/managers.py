from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class CreditoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Credito, db)


    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, diccionary):
        tipoCredito = TipoterrenoManager(self.db).obtener_x_nombre("Credito")

        diccionary['fktipoterreno'] = tipoCredito.id


        objeto = CreditoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Credito.", fecha=fecha, tabla="reserva",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, diccionary):
        objeto = CreditoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Credito.", fecha=fecha,tabla="reserva", identificador=a.id)
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


    def insert(self, diccionary):
        tipoCuota = TipoterrenoManager(self.db).obtener_x_nombre("Cuota")

        diccionary['fktipoterreno'] = tipoCuota.id


        objeto = CuotaManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Cuota.", fecha=fecha, tabla="reserva",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, diccionary):
        objeto = CuotaManager(self.db).entity(**diccionary)
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
