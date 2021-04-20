from ...operaciones.bitacora.managers import *
from .models import *
from server.common.managers import SuperManager
from server.ventas.reserva.models import *

from sqlalchemy.sql import func,or_,and_


class MonedaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Moneda, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, dictionary):
        objeto = MonedaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()
    
        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Moneda.", fecha=fecha, tabla="moneda",
                     identificador=a.id)
        super().insert(b)
    
        return a
    
    
    def update(self, dictionary):
        objeto = MonedaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()
    
        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Moneda.", fecha=fecha, tabla="moneda",
                     identificador=a.id)
        super().insert(b)
    
        return a
    
    
    def delete(self, id, Usuario, ip, enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()
    
        x.enabled = enable
    
        if enable:
            mensaje = "Se habilitó Moneda."
        else:
            mensaje = "Se deshabilitó Moneda."
    
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
    
        return mensaje