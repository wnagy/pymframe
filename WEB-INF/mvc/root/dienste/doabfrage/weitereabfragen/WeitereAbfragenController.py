# -*- coding: iso-8859-15 -*-
"""
Dieser Controller wird vom Framework aufgerufen.

Er ist fuer ein GRID Layout optimiert.

"""
from controller         import Controller
from helper.utility     import Utility


class WeitereAbfragenController(Controller):

   def get(self):
      self.view('info.tpl')
      

