import hashlib
from server.database.connection import transaction
from ..usuarios.rol.models import *


def insertions():
    with transaction() as session:
        flujo_m = session.query(Modulo).filter(Modulo.name == 'flujo').first()
        if flujo_m is None:
            flujo_m = Modulo(title='Reportes', name='flujo', icon='book')

        reporte_m = session.query(Modulo).filter(Modulo.name == 'reporte').first()
        if reporte_m is None:
            reporte_m = Modulo(title='Reportes', route='/reporte', name='reporte', icon='assessment')


        flujo_m.children.append(reporte_m)

        query_reporte = session.query(Modulo).filter(Modulo.name == 'reporte_query').first()
        if query_reporte is None:
            query_reporte = Modulo(title='Consultar', route='', name='reporte_query', menu=False)
        insert_reporte = session.query(Modulo).filter(Modulo.name == 'reporte_insert').first()
        if insert_reporte is None:
            insert_reporte = Modulo(title='Adicionar', route='/reporte_insert', name='reporte_insert', menu=False)
        update_reporte = session.query(Modulo).filter(Modulo.name == 'reporte_update').first()
        if update_reporte is None:
            update_reporte = Modulo(title='Actualizar', route='/reporte_update', name='reporte_update', menu=False)
        delete_reporte = session.query(Modulo).filter(Modulo.name == 'reporte_delete').first()
        if delete_reporte is None:
            delete_reporte = Modulo(title='Dar de Baja', route='/reporte_delete', name='reporte_delete', menu=False)
        imprimir_reporte = session.query(Modulo).filter(Modulo.name == 'reporte_imprimir').first()
        if imprimir_reporte is None:
            imprimir_reporte = Modulo(title='Reportes', route='/reporte_imprimir',
                                      name='reporte_imprimir',
                                      menu=False)

        reporte_m.children.append(query_reporte)
        reporte_m.children.append(insert_reporte)
        reporte_m.children.append(update_reporte)
        reporte_m.children.append(delete_reporte)
        reporte_m.children.append(imprimir_reporte)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        registrador_role = session.query(Rol).filter(Rol.nombre == 'REGISTRADOR').first()

        ###Modulo de Usuarios
        admin_role.modulos.append(flujo_m)
        admin_role.modulos.append(reporte_m)

        admin_role.modulos.append(query_reporte)
        admin_role.modulos.append(insert_reporte)
        admin_role.modulos.append(update_reporte)
        admin_role.modulos.append(delete_reporte)
        admin_role.modulos.append(imprimir_reporte)

        registrador_role.modulos.append(flujo_m)
        registrador_role.modulos.append(reporte_m)

        registrador_role.modulos.append(query_reporte)
        registrador_role.modulos.append(insert_reporte)
        registrador_role.modulos.append(update_reporte)
        registrador_role.modulos.append(delete_reporte)
        registrador_role.modulos.append(imprimir_reporte)


        session.commit()
