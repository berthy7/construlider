from .usuarios.usuario.controllers import *
from .usuarios.rol.controllers import *
from .usuarios.login.controllers import *

from .clientes.cliente.controllers import *

from .terrenos.terreno.controllers import *
from .terrenos.casa.controllers import *
from .terrenos.urbanizacion.controllers import *
from .terrenos.manzano.controllers import *

from .ventas.reserva.controllers import *
from .ventas.contrato.controllers import *
from .ventas.devolucion.controllers import *
from .ventas.credito.controllers import *
from .ventas.entidad.controllers import *

from .cobros.pago.controllers import *

from .flujo.reporte.controllers import *

from .parametros.moneda.controllers import *
from .parametros.ajuste.controllers import *


from server.operaciones.bitacora.controllers import *


from .main.controllers import Index
from tornado.web import StaticFileHandler

import os


def get_handlers():
    """Retorna una lista con las rutas, sus manejadores y datos extras."""
    handlers = list()
    # Login
    handlers.append((r'/login', LoginController))
    handlers.append((r'/logout', LogoutController))
    handlers.append((r'/manual', ManualController))

    # Principal
    handlers.append((r'/', Index))

    # Usuario
    handlers.extend(get_routes(UsuarioController))
    handlers.extend(get_routes(RolController))

    # Operaciones
    handlers.extend(get_routes(BitacoraController))

    # Clientes
    handlers.extend(get_routes(ClienteController))

    # Terrenos
    handlers.extend(get_routes(TerrenoController))
    handlers.extend(get_routes(CasaController))
    handlers.extend(get_routes(UrbanizacionController))
    handlers.extend(get_routes(ManzanoController))

    # Reserva ventas
    handlers.extend(get_routes(ReservaController))
    handlers.extend(get_routes(ContratoController))
    handlers.extend(get_routes(DevolucionController))
    handlers.extend(get_routes(CreditoController))
    handlers.extend(get_routes(EntidadController))

    # Cobros
    handlers.extend(get_routes(PagoController))

    # Flujo
    handlers.extend(get_routes(ReporteController))

    # Parametros
    handlers.extend(get_routes(MonedaController))
    handlers.extend(get_routes(AjusteController))


    # Recursos por submodulo
    handlers.append((r'/resources/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'resources')}))

    handlers.append((r'/common/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'assets')}))
    handlers.append((r'/main/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'main', 'assets')}))
    handlers.append((r'/operaciones/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'operaciones')}))
    handlers.append((r'/usuarios/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'usuarios')}))
    handlers.append((r'/clientes/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'clientes')}))
    handlers.append((r'/terrenos/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'terrenos')}))
    handlers.append((r'/ventas/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'ventas')}))
    handlers.append((r'/cobros/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'cobros')}))
    handlers.append((r'/flujo/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'flujo')}))
    handlers.append((r'/parametros/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'parametros')}))
    #Servicios Movil



    return handlers


def get_routes(handler):
    routes = list()
    for route in handler.routes:
        routes.append((route, handler))
    return routes
