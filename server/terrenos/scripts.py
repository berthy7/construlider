import hashlib
from server.database.connection import transaction
from ..usuarios.rol.models import *


def insertions():
    with transaction() as session:
        terrenos_m = session.query(Modulo).filter(Modulo.name == 'terrenos').first()
        if terrenos_m is None:
            terrenos_m = Modulo(title='Gestion de Terrenos', name='terrenos', icon='book')

        urbanizacion_m = session.query(Modulo).filter(Modulo.name == 'urbanizacion').first()
        if urbanizacion_m is None:
            urbanizacion_m = Modulo(title='Urbanizaciones', route='/urbanizacion', name='urbanizacion', icon='place')

        manzano_m = session.query(Modulo).filter(Modulo.name == 'manzano').first()
        if manzano_m is None:
            manzano_m = Modulo(title='Manzanos', route='/manzano', name='manzano', icon='place')

        terreno_m = session.query(Modulo).filter(Modulo.name == 'terreno').first()
        if terreno_m is None:
            terreno_m = Modulo(title='Terrenos', route='/terreno', name='terreno', icon='location_city')

        casa_m = session.query(Modulo).filter(Modulo.name == 'casa').first()
        if casa_m is None:
            casa_m = Modulo(title='Casas', route='/casa', name='casa', icon='home')



        terrenos_m.children.append(urbanizacion_m)
        terrenos_m.children.append(manzano_m)
        terrenos_m.children.append(terreno_m)
        terrenos_m.children.append(casa_m)







        query_urbanizacion = session.query(Modulo).filter(Modulo.name == 'urbanizacion_query').first()
        if query_urbanizacion is None:
            query_urbanizacion = Modulo(title='Consultar', route='', name='urbanizacion_query', menu=False)

        insert_urbanizacion = session.query(Modulo).filter(Modulo.name == 'urbanizacion_insert').first()
        if insert_urbanizacion is None:
            insert_urbanizacion = Modulo(title='Adicionar', route='/urbanizacion_insert', name='urbanizacion_insert',
                                         menu=False)

        update_urbanizacion = session.query(Modulo).filter(Modulo.name == 'urbanizacion_update').first()
        if update_urbanizacion is None:
            update_urbanizacion = Modulo(title='Actualizar', route='/urbanizacion_update', name='urbanizacion_update',
                                         menu=False)

        delete_urbanizacion = session.query(Modulo).filter(Modulo.name == 'urbanizacion_delete').first()
        if delete_urbanizacion is None:
            delete_urbanizacion = Modulo(title='Dar de Baja', route='/urbanizacion_delete', name='urbanizacion_delete',
                                         menu=False)

        urbanizacion_m.children.append(query_urbanizacion)
        urbanizacion_m.children.append(insert_urbanizacion)
        urbanizacion_m.children.append(update_urbanizacion)
        urbanizacion_m.children.append(delete_urbanizacion)

        query_manzano = session.query(Modulo).filter(Modulo.name == 'manzano_query').first()
        if query_manzano is None:
            query_manzano = Modulo(title='Consultar', route='', name='manzano_query', menu=False)

        insert_manzano = session.query(Modulo).filter(Modulo.name == 'manzano_insert').first()
        if insert_manzano is None:
            insert_manzano = Modulo(title='Adicionar', route='/manzano_insert', name='manzano_insert', menu=False)

        update_manzano = session.query(Modulo).filter(Modulo.name == 'manzano_update').first()
        if update_manzano is None:
            update_manzano = Modulo(title='Actualizar', route='/manzano_update', name='manzano_update', menu=False)

        delete_manzano = session.query(Modulo).filter(Modulo.name == 'manzano_delete').first()
        if delete_manzano is None:
            delete_manzano = Modulo(title='Dar de Baja', route='/manzano_delete', name='manzano_delete', menu=False)

        manzano_m.children.append(query_manzano)
        manzano_m.children.append(insert_manzano)
        manzano_m.children.append(update_manzano)
        manzano_m.children.append(delete_manzano)

        query_terreno = session.query(Modulo).filter(Modulo.name == 'terreno_query').first()
        if query_terreno is None:
            query_terreno = Modulo(title='Consultar', route='', name='terreno_query', menu=False)

        insert_terreno = session.query(Modulo).filter(Modulo.name == 'terreno_insert').first()
        if insert_terreno is None:
            insert_terreno = Modulo(title='Adicionar', route='/terreno_insert', name='terreno_insert', menu=False)

        update_terreno = session.query(Modulo).filter(Modulo.name == 'terreno_update').first()
        if update_terreno is None:
            update_terreno = Modulo(title='Actualizar', route='/terreno_update', name='terreno_update', menu=False)

        delete_terreno = session.query(Modulo).filter(Modulo.name == 'terreno_delete').first()
        if delete_terreno is None:
            delete_terreno = Modulo(title='Dar de Baja', route='/terreno_delete', name='terreno_delete', menu=False)

        terreno_m.children.append(query_terreno)
        terreno_m.children.append(insert_terreno)
        terreno_m.children.append(update_terreno)
        terreno_m.children.append(delete_terreno)

        query_casa = session.query(Modulo).filter(Modulo.name == 'casa_query').first()
        if query_casa is None:
            query_casa = Modulo(title='Consultar', route='', name='casa_query', menu=False)

        insert_casa = session.query(Modulo).filter(Modulo.name == 'casa_insert').first()
        if insert_casa is None:
            insert_casa = Modulo(title='Adicionar', route='/casa_insert', name='casa_insert', menu=False)

        update_casa = session.query(Modulo).filter(Modulo.name == 'casa_update').first()
        if update_casa is None:
            update_casa = Modulo(title='Actualizar', route='/casa_update', name='casa_update', menu=False)

        delete_casa = session.query(Modulo).filter(Modulo.name == 'casa_delete').first()
        if delete_casa is None:
            delete_casa = Modulo(title='Dar de Baja', route='/casa_delete', name='casa_delete', menu=False)

        casa_m.children.append(query_casa)
        casa_m.children.append(insert_casa)
        casa_m.children.append(update_casa)
        casa_m.children.append(delete_casa)

        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        registrador_role = session.query(Rol).filter(Rol.nombre == 'REGISTRADOR').first()

        ###Modulo de Usuarios
        admin_role.modulos.append(terrenos_m)
        admin_role.modulos.append(urbanizacion_m)
        admin_role.modulos.append(manzano_m)
        admin_role.modulos.append(terreno_m)
        admin_role.modulos.append(casa_m)

        admin_role.modulos.append(query_urbanizacion)
        admin_role.modulos.append(insert_urbanizacion)
        admin_role.modulos.append(update_urbanizacion)
        admin_role.modulos.append(delete_urbanizacion)

        admin_role.modulos.append(query_manzano)
        admin_role.modulos.append(insert_manzano)
        admin_role.modulos.append(update_manzano)
        admin_role.modulos.append(delete_manzano)

        admin_role.modulos.append(query_terreno)
        admin_role.modulos.append(insert_terreno)
        admin_role.modulos.append(update_terreno)
        admin_role.modulos.append(delete_terreno)

        admin_role.modulos.append(query_casa)
        admin_role.modulos.append(insert_casa)
        admin_role.modulos.append(update_casa)
        admin_role.modulos.append(delete_casa)

        registrador_role.modulos.append(terrenos_m)
        registrador_role.modulos.append(urbanizacion_m)
        registrador_role.modulos.append(manzano_m)
        registrador_role.modulos.append(terreno_m)
        registrador_role.modulos.append(casa_m)

        registrador_role.modulos.append(query_urbanizacion)
        registrador_role.modulos.append(query_manzano)
        registrador_role.modulos.append(query_terreno)
        registrador_role.modulos.append(query_casa)


        session.commit()
