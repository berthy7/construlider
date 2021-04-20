import hashlib
from server.database.connection import transaction
from ..usuarios.rol.models import *
from .moneda.models import *
from .ajuste.models import *


def insertions():
    with transaction() as session:
        parametros_m = session.query(Modulo).filter(Modulo.name == 'parametros').first()
        if parametros_m is None:
            parametros_m = Modulo(title='Parametros', name='parametros', icon='book')

        moneda_m = session.query(Modulo).filter(Modulo.name == 'moneda').first()
        if moneda_m is None:
            moneda_m = Modulo(title='Monedas', route='/moneda', name='moneda', icon='monetization_on')

        ajuste_m = session.query(Modulo).filter(Modulo.name == 'moneda').first()
        if ajuste_m is None:
            ajuste_m = Modulo(title='Ajustes', route='/ajuste', name='ajuste', icon='settings')


        parametros_m.children.append(moneda_m)
        parametros_m.children.append(ajuste_m)

        query_moneda = session.query(Modulo).filter(Modulo.name == 'moneda_query').first()
        if query_moneda is None:
            query_moneda = Modulo(title='Consultar', route='', name='moneda_query', menu=False)
        insert_moneda = session.query(Modulo).filter(Modulo.name == 'moneda_insert').first()
        if insert_moneda is None:
            insert_moneda = Modulo(title='Adicionar', route='/moneda_insert', name='moneda_insert', menu=False)
        update_moneda = session.query(Modulo).filter(Modulo.name == 'moneda_update').first()
        if update_moneda is None:
            update_moneda = Modulo(title='Actualizar', route='/moneda_update', name='moneda_update', menu=False)
        delete_moneda = session.query(Modulo).filter(Modulo.name == 'moneda_delete').first()
        if delete_moneda is None:
            delete_moneda = Modulo(title='Dar de Baja', route='/moneda_delete', name='moneda_delete', menu=False)
        imprimir_moneda = session.query(Modulo).filter(Modulo.name == 'moneda_imprimir').first()
        if imprimir_moneda is None:
            imprimir_moneda = Modulo(title='Reportes', route='/moneda_imprimir',
                                      name='moneda_imprimir',
                                      menu=False)

        moneda_m.children.append(query_moneda)
        moneda_m.children.append(insert_moneda)
        moneda_m.children.append(update_moneda)
        moneda_m.children.append(delete_moneda)
        moneda_m.children.append(imprimir_moneda)

        query_ajuste = session.query(Modulo).filter(Modulo.name == 'ajuste_query').first()
        if query_ajuste is None:
            query_ajuste = Modulo(title='Consultar', route='', name='ajuste_query', menu=False)
        insert_ajuste = session.query(Modulo).filter(Modulo.name == 'ajuste_insert').first()
        if insert_ajuste is None:
            insert_ajuste = Modulo(title='Adicionar', route='/ajuste_insert', name='ajuste_insert', menu=False)
        update_ajuste = session.query(Modulo).filter(Modulo.name == 'ajuste_update').first()
        if update_ajuste is None:
            update_ajuste = Modulo(title='Actualizar', route='/ajuste_update', name='ajuste_update', menu=False)
        delete_ajuste = session.query(Modulo).filter(Modulo.name == 'ajuste_delete').first()
        if delete_ajuste is None:
            delete_ajuste = Modulo(title='Dar de Baja', route='/ajuste_delete', name='ajuste_delete', menu=False)
        imprimir_ajuste = session.query(Modulo).filter(Modulo.name == 'ajuste_imprimir').first()
        if imprimir_ajuste is None:
            imprimir_ajuste = Modulo(title='Reportes', route='/ajuste_imprimir',
                                      name='ajuste_imprimir',
                                      menu=False)

        ajuste_m.children.append(query_ajuste)
        ajuste_m.children.append(insert_ajuste)
        ajuste_m.children.append(update_ajuste)
        ajuste_m.children.append(delete_ajuste)
        ajuste_m.children.append(imprimir_ajuste)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        registrador_role = session.query(Rol).filter(Rol.nombre == 'REGISTRADOR').first()

        ###Modulo de Usuarios
        admin_role.modulos.append(parametros_m)
        admin_role.modulos.append(moneda_m)
        admin_role.modulos.append(ajuste_m)

        admin_role.modulos.append(query_moneda)
        admin_role.modulos.append(insert_moneda)
        admin_role.modulos.append(update_moneda)
        admin_role.modulos.append(delete_moneda)
        admin_role.modulos.append(imprimir_moneda)

        admin_role.modulos.append(query_ajuste)
        admin_role.modulos.append(insert_ajuste)
        admin_role.modulos.append(update_ajuste)
        admin_role.modulos.append(delete_ajuste)
        admin_role.modulos.append(imprimir_ajuste)

        registrador_role.modulos.append(parametros_m)
        registrador_role.modulos.append(moneda_m)
        registrador_role.modulos.append(ajuste_m)

        registrador_role.modulos.append(query_moneda)
        registrador_role.modulos.append(insert_moneda)
        registrador_role.modulos.append(update_moneda)
        registrador_role.modulos.append(delete_moneda)
        registrador_role.modulos.append(imprimir_moneda)

        registrador_role.modulos.append(query_ajuste)
        registrador_role.modulos.append(insert_ajuste)
        registrador_role.modulos.append(update_ajuste)
        registrador_role.modulos.append(delete_ajuste)
        registrador_role.modulos.append(imprimir_ajuste)



        moneda1 = Moneda(nombre='Boliviano', codigo="Bs.")
        session.add(moneda1)
        session.commit()

        session.add(Moneda(nombre='Dolar', codigo="$", cambio=6.92,fktipoCambio=moneda1.id))

        session.add(Ajuste(montoMinimoReserva=100, fkmonedaReserva=2, tasaInteres=0.24, cuotasMora=3))

        session.commit()
