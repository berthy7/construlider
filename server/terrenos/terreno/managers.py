from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class TerrenoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Terreno, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.estado == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, diccionary):
        objeto = TerrenoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Terreno.", fecha=fecha, tabla="terreno",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, diccionary):
        objeto = TerrenoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Terreno.", fecha=fecha,tabla="terreno", identificador=a.id)
        super().insert(b)

        return a


