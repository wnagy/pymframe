# -*- coding: iso-8859-15 -*-
from controller import Controller

class ExtrasController(Controller):

   def get(self):
      self.view('view.tpl')
