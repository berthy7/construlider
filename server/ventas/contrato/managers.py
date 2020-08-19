from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class ContratoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Contrato, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.direccion.asc()).all()

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.direccion.asc()).all()


    def insert(self, diccionary):
        objeto = ContratoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Contrato.", fecha=fecha, tabla="contrato",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, diccionary):
        objeto = ContratoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

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
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


