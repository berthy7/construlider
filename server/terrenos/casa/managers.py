from ...operaciones.bitacora.managers import *
from server.terrenos.terreno.managers import *

from server.common.managers import SuperManager
from ..terreno.models import *
from sqlalchemy.sql import func,or_,and_


class CasaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Terreno, db)

    def verificar(self, idurbanizacion):
        u = self.db.query(Urbanizacion).filter(Urbanizacion.id == idurbanizacion).first()

        t = self.db.query(func.count(Terreno.id)).join(Manzano).join(Tipoterreno).filter(Manzano.fkurbanizacion == idurbanizacion).filter(Terreno.enabled == True).filter(Tipoterreno.nombre=="Casa").scalar()

        if u.numeroCasas > t:
            return dict(respuesta=True)

        else:
            return dict(respuesta=False)

    def list_all(self):
        return dict(objects=self.db.query(self.entity).join(Tipoterreno).filter(Tipoterreno.nombre=="Casa"))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.estado == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, dictionary):
        tipoTerreno = TipoterrenoManager(self.db).obtener_x_nombre("Casa")

        dictionary['fktipoterreno'] = tipoTerreno.id

        objeto = CasaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Casa.", fecha=fecha, tabla="terreno",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = CasaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Casa.", fecha=fecha,tabla="terreno", identificador=a.id)
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
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="terreno", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


