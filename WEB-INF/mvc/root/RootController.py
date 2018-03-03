# -*- coding: iso-8859-15 -*-
from controller import Controller

class RootController(Controller):

   def get(self):
      self.view('view.tpl')
