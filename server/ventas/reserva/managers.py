from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class ReservaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Reserva, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, diccionary):
        tipoReserva = ReservaManager(self.db).obtener_x_nombre("Reserva")

        diccionary['fktiporeserva'] = tipoReserva.id


        objeto = ReservaManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Reserva.", fecha=fecha, tabla="reserva",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, diccionary):
        objeto = ReservaManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Reserva.", fecha=fecha,tabla="reserva", identificador=a.id)
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

