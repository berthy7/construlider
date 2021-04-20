import hashlib
from server.database.connection import transaction
from ..usuarios.rol.models import *


def insertions():
    with transaction() as session:
        clientes_m = session.query(Modulo).filter(Modulo.name == 'clientes').first()
        if clientes_m is None:
            clientes_m = Modulo(title='Gestion de Clientes', name='clientes', icon='book')

        cliente_m = session.query(Modulo).filter(Modulo.name == 'cliente').first()
        if cliente_m is None:
            cliente_m = Modulo(title='Clientes', route='/cliente', name='cliente', icon='people_outline')


        clientes_m.children.append(cliente_m)

        query_cliente = session.query(Modulo).filter(Modulo.name == 'cliente_query').first()
        if query_cliente is None:
            query_cliente = Modulo(title='Consultar', route='', name='cliente_query', menu=False)
        insert_cliente = session.query(Modulo).filter(Modulo.name == 'cliente_insert').first()
        if insert_cliente is None:
            insert_cliente = Modulo(title='Adicionar', route='/cliente_insert', name='cliente_insert', menu=False)
        update_cliente = session.query(Modulo).filter(Modulo.name == 'cliente_update').first()
        if update_cliente is None:
            update_cliente = Modulo(title='Actualizar', route='/cliente_update', name='cliente_update', menu=False)
        delete_cliente = session.query(Modulo).filter(Modulo.name == 'cliente_delete').first()
        if delete_cliente is None:
            delete_cliente = Modulo(title='Dar de Baja', route='/cliente_delete', name='cliente_delete', menu=False)
        imprimir_cliente = session.query(Modulo).filter(Modulo.name == 'cliente_imprimir').first()
        if imprimir_cliente is None:
            imprimir_cliente = Modulo(title='Reportes', route='/cliente_imprimir',
                                      name='cliente_imprimir',
                                      menu=False)

        cliente_m.children.append(query_cliente)
        cliente_m.children.append(insert_cliente)
        cliente_m.children.append(update_cliente)
        cliente_m.children.append(delete_cliente)
        cliente_m.children.append(imprimir_cliente)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        registrador_role = session.query(Rol).filter(Rol.nombre == 'REGISTRADOR').first()

        ###Modulo de Usuarios
        admin_role.modulos.append(clientes_m)
        admin_role.modulos.append(cliente_m)

        admin_role.modulos.append(query_cliente)
        admin_role.modulos.append(insert_cliente)
        admin_role.modulos.append(update_cliente)
        admin_role.modulos.append(delete_cliente)
        admin_role.modulos.append(imprimir_cliente)

        registrador_role.modulos.append(clientes_m)
        registrador_role.modulos.append(cliente_m)

        registrador_role.modulos.append(query_cliente)
        registrador_role.modulos.append(insert_cliente)
        registrador_role.modulos.append(update_cliente)
        registrador_role.modulos.append(delete_cliente)
        registrador_role.modulos.append(imprimir_cliente)

        session.commit()
