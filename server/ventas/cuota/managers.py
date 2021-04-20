from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from server.ventas.credito.managers import *
from .models import *
from sqlalchemy.sql import func,or_,and_


class CuotaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Cuota, db)


    def cambiar_estado(self,id,estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        estadocuota = EstadocuotaManager(self.db).obtener_x_nombre(estado)
        x.fkestadocuota = estadocuota.id

        self.db.merge(x)
        self.db.commit()

        return x


    def listar_estado_pendiente_x_credito(self,idCredito):
        return self.db.query(self.entity).join(Estadocuota).filter(self.entity.fkcredito == idCredito).filter(Estadocuota.nombre != "Pagada").all()


    def listar_todo(self):
        print('listar todo cuota')
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()


    def insert(self, dictionary):
        tipoCuota = TipoterrenoManager(self.db).obtener_x_nombre("Cuota")

        dictionary['fktipoterreno'] = tipoCuota.id


        objeto = CuotaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Cuota.", fecha=fecha, tabla="cuota",
                     identificador=a.id)
        super().insert(b)


        return a


    def update(self, dictionary):
        objeto = CuotaManager(self.db).entity(**dictionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Cuota.", fecha=fecha,tabla="cuota", identificador=a.id)
        super().insert(b)

        return a


    def delete(self, id, Usuario, ip,enable):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.enabled = enable

        if enable:
            mensaje = "Se habilitó cuota."
        else:
            mensaje = "Se deshabilitó cuota."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion=mensaje, fecha=fecha,tabla="cuota", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return mensaje


    def actualizar_cuotas(self):
        fechadate = datetime.now(pytz.timezone('America/La_Paz'))
        fecha_hoy_str = fechadate.strftime('%Y-%m-%d %H:%M:%S')
        fechahoy = fecha_hoy_str[0:10]

        fechahoy = datetime.strptime(fechahoy, '%Y-%m-%d')

        cuotas = self.db.query(self.entity).join(Estadocuota).filter(self.entity.enabled == True).filter(Estadocuota.nombre == "Pendiente").filter(self.entity.fechaVencimiento < fechahoy).all()

        for x in cuotas:

            estadocuota = EstadocuotaManager(self.db).obtener_x_nombre("Mora")
            x.fkestadocuota  = estadocuota.id

            self.db.merge(x)
        self.db.commit()


class EstadocuotaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Estadocuota, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()


    def obtener_x_nombre(self,nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(self.entity.enabled == True).first()


