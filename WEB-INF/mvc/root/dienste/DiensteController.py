# -*- coding: iso-8859-15 -*-
"""
Dieser Controller wird vom Framework aufgerufen.

Er ist fuer ein GRID Layout optimiert.

"""
from controller         import Controller
from viewhandler        import Viewhandler
from helper.utility     import Utility


class DiensteController(Controller):

   viewhandler = None

   def get(self):
      self.view('info.tpl')
      

