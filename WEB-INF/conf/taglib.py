# -*- coding: iso-8859-15 -*-

"""
Diese Klasse erbt von der Taglib Basisklasse
und dient zur Erweiterung fuer anwendungsspezifische
Funktionen
"""
from taglibbase import TaglibBase
from dateconverter import Dateconverter

class Taglib(TaglibBase):

   def getCurrentDate(self):
      """
      Liefert heutiges Datum
      """
      dc = Dateconverter()
      return dc.giveAsGermanDate('now')
   

   def getFilter(self,text=None,path=None,default=''):
      """
      Liefert eine Kriteriumsmaske mit Filterfeld

      @param   text  Text, welcher vor dem Inputfeld ausgegeben wird
      @param   path  Pfad

      @return  Div mit Kriterienmaske
      """
      
      text = '' if text==None else text

      tpl = '<div class="kriterien">&nbsp;{0}\
               <input type="hidden" name="path" value="{1}"/>\
               &nbsp;{2}\
               <input type="text" name="_filter" value="{3}"/>\
               <input type="submit" value="Filtern">{4}</div>'
      retval = tpl.format(self.form(),path,text,default,self.endform())
      
      return retval