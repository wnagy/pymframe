# -*- coding: iso-8859-15 -*-
from dbaccess.core   import *

class LovDomain(Domain) :
   lovID     = None
   lovClass  = None
   lovKey    = None
   lovValue  = None
   lovFlag1  = None
   lovFlag2  = None
   lovFlag3  = None
   lovFlag4  = None
   lovRemark = None

   meta = {
      'tablename':'lov',
      'primarykey':'lovID',

      'fields':{
         'lovID'       : {'dbfield':'lovID',          'type':'Integer'},
         'lovClass'    : {'dbfield':'lovClass',       'type':'String'},
         'lovKey'      : {'dbfield':'lovKey',         'type':'String'},
         'lovValue'    : {'dbfield':'lovValue',       'type':'String'},
         'lovFlag1'    : {'dbfield':'lovFlag1',       'type':'String'},
         'lovFlag2'    : {'dbfield':'lovFlag2',       'type':'String'},
         'lovFlag3'    : {'dbfield':'lovFlag3',       'type':'String'},
         'lovFlag4'    : {'dbfield':'lovFlag4',       'type':'String'},
         'lovRemark'   : {'dbfield':'lovRemark',      'type':'String'}
         }
      }
   def getDatasourceClass(self,addempty=None):
      retval = list()
      where = "lovClass='CLASS'"
      if addempty != None:
         retval.append(['0',addempty])
      for lov in self.eachDomain(where=where,orderby='lovKey'):
         retval.append([lov.lovKey,lov.lovKey])

      return retval

   def truncate(self,value,size):
      if len(value) > size :
         value = value[:size]
         while ord(value[-1]) > 127: value = value[:-1]
         value += '&hellip;'
      return value
      
   def getDatasource(self,theClass,addempty=None,orderby='lovKey',truncate=None):
      
      retval = list()
      where = "lovClass='{0}'".format(theClass)
      
      if addempty != None:
         retval.append(['',addempty])

      for lov in self.eachDomain(where=where,orderby=orderby):

         title = None

         if truncate is not None:
            text = self.truncate(lov.lovValue,truncate)
            title = lov.lovValue
         else:
            text = lov.lovValue

         option = {
            'value':lov.lovKey,
            'text':text,
            'title':title
            }
         retval.append(option)
      
      return retval

   
   def getLovValue (self,lovClass,lovKey):
      """
      Liefert ueber eine Klasse und Key den Inhalt.

      @param   lovClass       Klasse
      @param   lovKey         Schluessel

      @return     Wert, oder None wenn nicht gefunden.

      """
      lov = LovDomain(self.db)

      where = "lovClass='{0}' and lovKey='{1}'".format(lovClass,lovKey)
      
      lov.get(where=where)
      if lov.isOk:
         return lov.lovValue
      else:
         return None
