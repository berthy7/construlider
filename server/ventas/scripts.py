import hashlib
from server.database.connection import transaction
from ..usuarios.rol.models import *
from server.terrenos.terreno.models import *


def insertions():
    with transaction() as session:
        ventas_m = session.query(Modulo).filter(Modulo.name == 'ventas').first()
        if ventas_m is None:
            ventas_m = Modulo(title='Reservas y Ventas', name='ventas', icon='book')

        reserva_m = session.query(Modulo).filter(Modulo.name == 'reserva').first()
        if reserva_m is None:
            reserva_m = Modulo(title='Reservas', route='/reserva', name='reserva', icon='done')

        contrato_m = session.query(Modulo).filter(Modulo.name == 'contrato').first()
        if contrato_m is None:
            contrato_m = Modulo(title='Ventas', route='/contrato', name='contrato', icon='done_all')

        credito_m = session.query(Modulo).filter(Modulo.name == 'credito').first()
        if credito_m is None:
            credito_m = Modulo(title='Plan de pagos', route='/credito', name='credito', icon='content_paste')

        entidad_m = session.query(Modulo).filter(Modulo.name == 'contrato').first()
        if entidad_m is None:
            entidad_m = Modulo(title='Entidades', route='/entidad', name='entidad', icon='account_balance')

        ventas_m.children.append(reserva_m)
        ventas_m.children.append(contrato_m)
        ventas_m.children.append(credito_m)
        ventas_m.children.append(entidad_m)

        query_reserva = session.query(Modulo).filter(Modulo.name == 'reserva_query').first()
        if query_reserva is None:
            query_reserva = Modulo(title='Consultar', route='', name='reserva_query', menu=False)

        insert_reserva = session.query(Modulo).filter(Modulo.name == 'reserva_insert').first()
        if insert_reserva is None:
            insert_reserva = Modulo(title='Adicionar', route='/reserva_insert', name='reserva_insert',
                                         menu=False)

        update_reserva = session.query(Modulo).filter(Modulo.name == 'reserva_update').first()
        if update_reserva is None:
            update_reserva = Modulo(title='Actualizar', route='/reserva_update', name='reserva_update',
                                         menu=False)

        delete_reserva = session.query(Modulo).filter(Modulo.name == 'reserva_delete').first()
        if delete_reserva is None:
            delete_reserva = Modulo(title='Dar de Baja', route='/reserva_delete', name='reserva_delete',
                                         menu=False)

        reserva_m.children.append(query_reserva)
        reserva_m.children.append(insert_reserva)
        reserva_m.children.append(update_reserva)
        reserva_m.children.append(delete_reserva)

        query_contrato = session.query(Modulo).filter(Modulo.name == 'contrato_query').first()
        if query_contrato is None:
            query_contrato = Modulo(title='Consultar', route='', name='contrato_query', menu=False)

        insert_contrato = session.query(Modulo).filter(Modulo.name == 'contrato_insert').first()
        if insert_contrato is None:
            insert_contrato = Modulo(title='Adicionar', route='/contrato_insert', name='contrato_insert',
                                         menu=False)

        update_contrato = session.query(Modulo).filter(Modulo.name == 'contrato_update').first()
        if update_contrato is None:
            update_contrato = Modulo(title='Actualizar', route='/contrato_update', name='contrato_update',
                                         menu=False)

        delete_contrato = session.query(Modulo).filter(Modulo.name == 'contrato_delete').first()
        if delete_contrato is None:
            delete_contrato = Modulo(title='Dar de Baja', route='/contrato_delete', name='contrato_delete',
                                         menu=False)

        contrato_m.children.append(query_contrato)
        contrato_m.children.append(insert_contrato)
        contrato_m.children.append(update_contrato)
        contrato_m.children.append(delete_contrato)

        query_credito = session.query(Modulo).filter(Modulo.name == 'credito_query').first()
        if query_credito is None:
            query_credito = Modulo(title='Consultar', route='', name='credito_query', menu=False)

        insert_credito = session.query(Modulo).filter(Modulo.name == 'credito_insert').first()
        if insert_credito is None:
            insert_credito = Modulo(title='Adicionar', route='/credito_insert', name='credito_insert',
                                         menu=False)

        update_credito = session.query(Modulo).filter(Modulo.name == 'credito_update').first()
        if update_credito is None:
            update_credito = Modulo(title='Actualizar', route='/credito_update', name='credito_update',
                                         menu=False)

        delete_credito = session.query(Modulo).filter(Modulo.name == 'credito_delete').first()
        if delete_credito is None:
            delete_credito = Modulo(title='Dar de Baja', route='/credito_delete', name='credito_delete',
                                         menu=False)

        credito_m.children.append(query_credito)
        credito_m.children.append(insert_credito)
        credito_m.children.append(update_credito)
        credito_m.children.append(delete_credito)

        query_entidad = session.query(Modulo).filter(Modulo.name == 'entidad_query').first()
        if query_entidad is None:
            query_entidad = Modulo(title='Consultar', route='', name='entidad_query', menu=False)

        insert_entidad = session.query(Modulo).filter(Modulo.name == 'entidad_insert').first()
        if insert_entidad is None:
            insert_entidad = Modulo(title='Adicionar', route='/entidad_insert', name='entidad_insert',
                                         menu=False)

        update_entidad = session.query(Modulo).filter(Modulo.name == 'entidad_update').first()
        if update_entidad is None:
            update_entidad = Modulo(title='Actualizar', route='/entidad_update', name='entidad_update',
                                         menu=False)

        delete_entidad = session.query(Modulo).filter(Modulo.name == 'entidad_delete').first()
        if delete_entidad is None:
            delete_entidad = Modulo(title='Dar de Baja', route='/entidad_delete', name='entidad_delete',
                                         menu=False)

        entidad_m.children.append(query_entidad)
        entidad_m.children.append(insert_entidad)
        entidad_m.children.append(update_entidad)
        entidad_m.children.append(delete_entidad)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        registrador_role = session.query(Rol).filter(Rol.nombre == 'REGISTRADOR').first()

        ###Modulo de Usuarios
        admin_role.modulos.append(ventas_m)
        admin_role.modulos.append(reserva_m)
        admin_role.modulos.append(contrato_m)
        admin_role.modulos.append(credito_m)
        admin_role.modulos.append(entidad_m)


        admin_role.modulos.append(query_reserva)
        admin_role.modulos.append(insert_reserva)
        admin_role.modulos.append(update_reserva)
        admin_role.modulos.append(delete_reserva)

        admin_role.modulos.append(query_contrato)
        admin_role.modulos.append(insert_contrato)
        admin_role.modulos.append(update_contrato)
        admin_role.modulos.append(delete_contrato)

        admin_role.modulos.append(query_credito)
        admin_role.modulos.append(insert_credito)
        admin_role.modulos.append(update_credito)
        admin_role.modulos.append(delete_credito)

        admin_role.modulos.append(query_entidad)
        admin_role.modulos.append(insert_entidad)
        admin_role.modulos.append(update_entidad)
        admin_role.modulos.append(delete_entidad)


        registrador_role.modulos.append(ventas_m)
        registrador_role.modulos.append(reserva_m)
        registrador_role.modulos.append(contrato_m)
        registrador_role.modulos.append(credito_m)
        registrador_role.modulos.append(entidad_m)

        registrador_role.modulos.append(query_reserva)
        registrador_role.modulos.append(insert_reserva)
        registrador_role.modulos.append(update_reserva)
        registrador_role.modulos.append(delete_reserva)

        registrador_role.modulos.append(query_contrato)
        registrador_role.modulos.append(insert_contrato)
        registrador_role.modulos.append(update_contrato)
        registrador_role.modulos.append(delete_contrato)

        registrador_role.modulos.append(query_credito)
        registrador_role.modulos.append(insert_credito)
        registrador_role.modulos.append(update_credito)
        registrador_role.modulos.append(delete_credito)

        registrador_role.modulos.append(query_entidad)
        registrador_role.modulos.append(insert_entidad)
        registrador_role.modulos.append(update_entidad)
        registrador_role.modulos.append(delete_entidad)


        session.commit()
