from ...operaciones.bitacora.managers import *
from server.terrenos.terreno.managers import *

from server.common.managers import SuperManager
from ..terreno.models import *
from sqlalchemy.sql import func,or_,and_


class CasaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Terreno, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity).join(Tipoterreno).filter(Tipoterreno.nombre=="Casa"))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.estado == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, diccionary):
        tipoTerreno = TipoterrenoManager(self.db).obtener_x_nombre("Casa")

        diccionary['fktipoterreno'] = tipoTerreno.id

        objeto = CasaManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Casa.", fecha=fecha, tabla="casa",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, diccionary):
        objeto = CasaManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Casa.", fecha=fecha,tabla="casa", identificador=a.id)
        super().insert(b)

        return a

    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó casa."
        else:
            mensaje = "Se deshabilitó casa."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


