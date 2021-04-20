from ...operaciones.bitacora.managers import *
from server.terrenos.urbanizacion.models import *
from server.terrenos.manzano.models import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,or_,and_


class TerrenoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Terreno, db)

    def verificar(self, idurbanizacion):
        u = self.db.query(Urbanizacion).filter(Urbanizacion.id == idurbanizacion).first()

        t = self.db.query(func.count(Terreno.id)).join(Manzano).join(Tipoterreno).filter(Manzano.fkurbanizacion == idurbanizacion).filter(Terreno.enabled == True).filter(Tipoterreno.nombre=="Terreno").scalar()

        if u.numeroTerrenos > t:
            return dict(respuesta=True)

        else:
            return dict(respuesta=False)

    def list_all(self):
        return dict(objects=self.db.query(self.entity).join(Tipoterreno).filter(Tipoterreno.nombre=="Terreno"))

    def listar_x_manzano(self, idmanzano,idtipoterreno,idterreno):

        x = self.db.query(self.entity).filter(self.entity.estado == True).filter(self.entity.enabled == True).filter(
            self.entity.fkmanzano == idmanzano).filter(self.entity.fktipoterreno == idtipoterreno).all()

        if idterreno:

            if self.db.query(self.entity).filter(self.entity.id == idterreno).filter(
            self.entity.fkmanzano == idmanzano).filter(self.entity.fktipoterreno == idtipoterreno).first():

                x.append(self.db.query(self.entity).filter(self.entity.id == idterreno).filter(
                self.entity.fkmanzano == idmanzano).filter(self.entity.fktipoterreno == idtipoterreno).first())

        return x


    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.estado == True).all()


    def cambiar_estado(self,id,estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.estado = estado
        self.db.merge(x)
        self.db.commit()

        return x


    def insert(self, dictionary):
        tipoTerreno = TipoterrenoManager(self.db).obtener_x_nombre("Terreno")

        dictionary['fktipoterreno'] = tipoTerreno.id


        objeto = TerrenoManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Terreno.", fecha=fecha, tabla="terreno",
                     identificador=a.id)
        super().insert(b)


        return a

    def update(self, dictionary):
        objeto = TerrenoManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Terreno.", fecha=fecha,tabla="terreno", identificador=a.id)
        super().insert(b)

        return a

    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó terreno."
        else:
            mensaje = "Se deshabilitó terreno."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="terreno", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


class TipoterrenoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Tipoterreno, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def obtener_x_nombre(self,nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(self.entity.enabled == True).first()


