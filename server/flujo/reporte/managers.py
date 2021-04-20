from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from server.ventas.reserva.models import *

from sqlalchemy.sql import func,or_,and_


class ReporteManager(SuperManager):
    def __init__(self, db):
        super().__init__(Reserva, db)

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()
