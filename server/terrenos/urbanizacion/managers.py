from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class UrbanizacionManager(SuperManager):
    def __init__(self, db):
        super().__init__(Urbanizacion, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.direccion.asc()).all()

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.direccion.asc()).all()


    def insert(self, dictionary):
        objeto = UrbanizacionManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Urbanizacion.", fecha=fecha, tabla="urbanizacion",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = UrbanizacionManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Urbanizacion.", fecha=fecha,tabla="urbanizacion", identificador=a.id)
        super().insert(b)

        return a

    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó Urbanizacion."
        else:
            mensaje = "Se deshabilitó Urbanizacion."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="urbanizacion", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


