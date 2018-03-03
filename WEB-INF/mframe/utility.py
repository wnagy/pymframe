# -*- coding: iso-8859-15 -*-

"""
Verschiedene Hilfsroutinen 
"""

class Utility (object):
   
   def objectFactory(self):
      """
      Erzeugen eines leeren Objekts

      HINT:
         in Python Golf
      """
      return type('', (), {})()

   def fieldsObjectFactory(self,domain,nullisempty=True):
      """
      Kopiert alle Datenfelder eine Domain in ein Objekt
      und gibt dieses zurueck.

      @param   domain         Domain
      @param   nullisemtpy    Ist ein Feld None wird "" geliefert
      @return  Ein Objekt mit allen Inhalten der uebergebenen Domain
      """

      # erzeugen eines leeren Objekts
      result = self.objectFactory()

      # Kopieren der Feldinhalte einer Domain in 
      # ein dynamisch erzeugtes Objekt
      for key in domain.meta['fields']:
         value = domain.__dict__[key]
         if value is None: value = ''
         setattr(result,key,domain.__dict__[key])
      return result
