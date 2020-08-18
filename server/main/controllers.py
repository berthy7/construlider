from server.database.connection import transaction
from tornado.web import authenticated
from tornado.gen import coroutine
from server.common.utils import decorators
from ..common.controllers import SuperController
from threading import Thread
from datetime import datetime, timedelta, time, date
import pytz
from ..usuarios.usuario.managers import *


class Index(SuperController):

    @decorators(authenticated, coroutine)
    def get(self):
        try:
            usuario = self.get_user()
            if usuario:
                self.render("main/index.html", user=usuario)
            else:
                self.redirect('/logout')
        except Exception as e:
            print(e)
            self.redirect('/logout')
