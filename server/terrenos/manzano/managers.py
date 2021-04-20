from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class ManzanoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Manzano, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def listar_x_urbanizacion(self, idurbanizacion):

        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkurbanizacion == idurbanizacion)\
            .order_by(self.entity.numero.asc()).all()


    def insert(self, dictionary):
        objeto = ManzanoManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Manzano.", fecha=fecha, tabla="manzano",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = ManzanoManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Manzano.", fecha=fecha,tabla="manzano", identificador=a.id)
        super().insert(b)

        return a

    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó Manzano."
        else:
            mensaje = "Se deshabilitó Manzano."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="manzano", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje





