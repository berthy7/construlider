import hashlib
from server.database.connection import transaction
from ..usuarios.rol.models import *
from server.cobros.pago.models import *


def insertions():
    with transaction() as session:
        cobros_m = session.query(Modulo).filter(Modulo.name == 'cobros').first()
        if cobros_m is None:
            cobros_m = Modulo(title='Cobros', name='cobros', icon='book')

        pago_m = session.query(Modulo).filter(Modulo.name == 'pago').first()
        if pago_m is None:
            pago_m = Modulo(title='Pagos', route='/pago', name='pago', icon='attach_money')


        cobros_m.children.append(pago_m)

        query_pago = session.query(Modulo).filter(Modulo.name == 'pago_query').first()
        if query_pago is None:
            query_pago = Modulo(title='Consultar', route='', name='pago_query', menu=False)
        insert_pago = session.query(Modulo).filter(Modulo.name == 'pago_insert').first()
        if insert_pago is None:
            insert_pago = Modulo(title='Adicionar', route='/pago_insert', name='pago_insert', menu=False)
        update_pago = session.query(Modulo).filter(Modulo.name == 'pago_update').first()
        if update_pago is None:
            update_pago = Modulo(title='Actualizar', route='/pago_update', name='pago_update', menu=False)
        delete_pago = session.query(Modulo).filter(Modulo.name == 'pago_delete').first()
        if delete_pago is None:
            delete_pago = Modulo(title='Dar de Baja', route='/pago_delete', name='pago_delete', menu=False)
        imprimir_pago = session.query(Modulo).filter(Modulo.name == 'pago_imprimir').first()
        if imprimir_pago is None:
            imprimir_pago = Modulo(title='Reportes', route='/pago_imprimir',
                                      name='pago_imprimir',
                                      menu=False)

        pago_m.children.append(query_pago)
        pago_m.children.append(insert_pago)
        pago_m.children.append(update_pago)
        pago_m.children.append(delete_pago)
        pago_m.children.append(imprimir_pago)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        registrador_role = session.query(Rol).filter(Rol.nombre == 'REGISTRADOR').first()

        ###Modulo de Usuarios
        admin_role.modulos.append(cobros_m)
        admin_role.modulos.append(pago_m)

        admin_role.modulos.append(query_pago)
        admin_role.modulos.append(insert_pago)
        admin_role.modulos.append(update_pago)
        admin_role.modulos.append(delete_pago)
        admin_role.modulos.append(imprimir_pago)

        registrador_role.modulos.append(cobros_m)
        registrador_role.modulos.append(pago_m)

        registrador_role.modulos.append(query_pago)
        registrador_role.modulos.append(insert_pago)
        registrador_role.modulos.append(update_pago)
        registrador_role.modulos.append(delete_pago)
        registrador_role.modulos.append(imprimir_pago)

        session.add(Tipopago(nombre='Contado'))
        session.add(Tipopago(nombre='Transferencia'))

        session.commit()
