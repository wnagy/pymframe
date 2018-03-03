# -*- coding: iso-8859-15 -*-
from dbaccess.core   import *

class %(domain)s(Domain):
   %(key)s = None

   meta = {
      'tablename':'%(table)s',
      'primarykey':'%(key)s',
      'fields':{
         '%(key)s'             : {'dbfield':'%(key)s',           'type':'Integer'},
      }
   }

   def getDatasource(self,selected=None):
      """
      Erzeugt eine Datasource fuer die Verwendung in
      taglib.promptinput
      """
      retval = []
      for domain in self.eachDomain(where=None,orderby=None):
         retval.append([domain.%(key)s,domain.%(key)s])
      return retval

   # ### HANDLER
   #
   #     HINT:
   #        Handler liefern [True|False] Zurueck.
   #        Bei False wird die Datenbankaktion abgebrochen
   #
   #     Diese Methoden koennen, wenn sie nicht benoetigt wereden
   #     aus dieser Datei entfernt werden.
   #
   #     Fehlermeldungen koennen mit self.addError("Meldung")
   #     angegben werden.
   #
   def onCgiField(self,fieldname,value):
      """
      Wenn die Domain ueber das CGI befuellt wir
      wird bei jedem Feld dieser Handler aufgerufen.


      @param fieldname         Feldname
      @param value             Inhalt aus dem CGI

      @param [True|False]      wird False uebergeben so bricht das Laden ab
      """
      return True

  
   def onReadFromCgi(self,fieldname,value):
      """
      Veraender eines eingelesenen Wertes

      @param fieldname         Feldname
      @param value             Inhalt aus dem CGI

      @return  Veraendertet Inhalt aus dem CGI
      """
      return value
      
   def afterCgi(self):
      """
      Wird nach dem Einlesen aller Felder aus dem CGI
      aufgerufen.

      @return  [True|False]
      """
      return True

   def onDelete(self):
      """
      Wird aufgerufen vor Loeschen eines Datensatzens

      @return [True|False]
      """
      return True

   def onInsert(self):
      """
      Wird aufgerufen vor Einfuegen eines Datensatzens
      False beendet die Aktion

      @return [True|False]

      """
      return True

   def onUpdate(self):
      """
      Wird aufgerufen vor Veraendern eines Datensatzens
      False beendet die Aktion

      @return [True|False]

      """
      return True

   def onWrite(self,mode=None):
      """
      Wird vor jeder schreibenden
      Operation aufgerfuen.

      @param  mode     Enthaelt insert/update/delete

      @return [True|False]

      """
      return True

   #
   # ################# END OF HANDLER
