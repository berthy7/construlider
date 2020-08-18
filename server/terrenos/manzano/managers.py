from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class ManzanoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Manzano, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.estado == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, diccionary):
        objeto = ManzanoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Manzano.", fecha=fecha, tabla="cliente",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, diccionary):
        objeto = ManzanoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Manzano.", fecha=fecha,tabla="cliente", identificador=a.id)
        super().insert(b)

        return a


