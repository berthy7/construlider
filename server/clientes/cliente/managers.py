from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class ClienteManager(SuperManager):
    def __init__(self, db):
        super().__init__(Cliente, db)

    def listar_todo(self):
        print('listar_todo')
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, dictionary):
        objeto = ClienteManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Cliente.", fecha=fecha, tabla="cliente",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = ClienteManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Cliente.", fecha=fecha,tabla="cliente", identificador=a.id)
        super().insert(b)

        return a


    def delete(self, id, Usuario, ip, enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó Cliente."
        else:
            mensaje = "Se deshabilitó Cliente."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="cliente", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje

