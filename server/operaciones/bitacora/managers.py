from server.common.managers import SuperManager
from server.usuarios.usuario.models import *
from .models import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pytz
import calendar

class BitacoraManager(SuperManager):

    def __init__(self, db):
        super().__init__(Bitacora, db)

    def list_all(self):
        return dict(objects=self.db.query(Bitacora).order_by(Bitacora.id.asc()))

    def fecha_actual(self):

        fechaHora = datetime.now(pytz.timezone('America/La_Paz'))


        fecha_str = str(fechaHora)
        fecha_ = fecha_str[0:19]
        fechaHora = datetime.strptime(fecha_, '%Y-%m-%d %H:%M:%S')

        timezone = pytz.timezone('America/La_Paz')
        fechaHora = pytz.utc.localize(fechaHora, is_dst=None).astimezone(timezone)

        return fechaHora

    def fecha(self):
        fechaHora = datetime.now(pytz.timezone('America/La_Paz'))

        fecha_str = str(fechaHora)
        fecha_ = fecha_str[0:19]
        fechaHora = datetime.strptime(fecha_, '%Y-%m-%d %H:%M:%S')

        timezone = pytz.timezone('America/La_Paz')
        fechaHora = pytz.utc.localize(fechaHora, is_dst=None).astimezone(timezone)

        return fechaHora

    def obtener_dia(self,fecha):

        dia = calendar.day_name[fecha.weekday()]

        if dia == "Monday":
            dia = "Lu"
        elif dia == "Tuesday":
            dia = "Ma"
        elif dia == "Wednesday":
            dia = "Mi"
        elif dia == "Thursday":
            dia = "Ju"
        elif dia == "Friday":
            dia = "Vi"
        elif dia == "Saturday":
            dia = "Sa"
        elif dia == "Sunday":
            dia = "Do"

        return dia

    def rango_fechas(self,fechai, fechaf):
        rango = []
        dias_totales = (fechaf - fechai).days
        for days in range(dias_totales + 1):
            fecha = fechai + relativedelta(days=days)
            rango.append(fecha)
        return rango
