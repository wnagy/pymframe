# -*- coding: iso-8859-15 -*-
"""
Dieser Controller wird vom Framework aufgerufen.

Er ist fuer ein GRID Layout optimiert.

"""
from controller         import Controller
from viewhandler        import Viewhandler
from helper.utility     import Utility

from domain.{2} import {1}


class {0}Controller(Controller):

   viewhandler = None

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
         controller  = self,                                      # Die Methoden des Controllers
         layout      = Viewhandler.GRID_LAYOUT,                   # Layout [GRID_LAYOUT|LISTEDIT_LAYOUT]
         domain      = {1}(db=self.db),
         where       = None,                                      # Where Klausel fuer SQL
         orderby     = None,                                      # Order by Klausel fuer SQL
         listparam   = None,                                      # Uebergabeparameter fuer Grid-Viewer als Dictionary
         gridlist    = None,                                      # Handler fuer die Datengewinnung der Ausgabeliste (wird automatisch erzeugt wenn None)
         filter=Utility.normalizeFilter(self.cgiparam('_filter')) # Globaler Filter

         )

      # aufrufen des Handlers
      self.viewhandler.run()
