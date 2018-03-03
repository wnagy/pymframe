# -*- coding: iso-8859-15 -*-
"""
Dieser Controller wird vom Framework aufgerufen.

Er ist fuer ein GRID Layout optimiert.

"""
from controller         import Controller
from viewhandler        import Viewhandler
from helper.utility     import Utility

from domain.lovdomain import LovDomain


class LovController(Controller):

   viewhandler = None

   def getWhere(self):
      lov = LovDomain(self.db)
      where = '(1=1)'
      
      if self.cgiparam('_class') != '0':
         where += " AND lovClass = '{0}' ".format(self.cgiparam('_class'))
      
      return where      

   
   def get(self):
      """
      Einsprungspunkt auf dem Framework.
      """
      #
      # Erzeugen des Viewhandlers
      # Parameter mit None werden vom Konstruktor automatisch
      # behandelt.
      #

      self.viewhandler = Viewhandler(
         controller  = self,
         layout      = Viewhandler.GRID_LAYOUT,
         domain      = LovDomain(db=self.db),
         where       = self.getWhere(),
         orderby     = None,
         listparam   = None,
         gridlist    = None,
         filter=Utility.normalizeFilter(self.cgiparam('_filter'))

         )

      # aufrufen des Handlers
      self.viewhandler.run()

