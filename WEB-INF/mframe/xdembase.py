# -*- coding: utf-8 -*-

"""
Basisklasse fuer xDEM Schnittstellenspezifikation

xDEM ist eine RPC Schnittstelle zum Uebertragen von strukturierten Daten
zwischen Datenbanken.

Dieses Klasse ist fuer MS Excel Schnittstellen Dateien vorbereitet
"""

import   time
import   sys
import   codecs

class XdemDomainImportBase(object):

   PRG            = dict()
   IFN            = None
   COL            = None
   domain         = None
   db             = None
   errors         = list()
   typecheckStrict=True
   xlsEncoding    = 'utf-8'
   comd           = None
 

   # Zu xlrd kompatible Datentypen
   XL_CELL_EMPTY     =0 # empty string u''
   XL_CELL_TEXT      =1 # a Unicode string
   XL_CELL_NUMBER    =2 # float
   XL_CELL_DATE      =3 # float
   XL_CELL_BOOLEAN   =4 # int; 1 means TRUE, 0 means FALSE
   XL_CELL_ERROR     =5 # int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code
   XL_CELL_BLANK     =6 # empty string u''. Note: this type will appear only when open_workbook(..., formatting_info=True) is used.


   def getCol(self,row,col):
      """
      Gibt den Inhalt der Zelle oder None wenn nicht erreichbar.
      """
      
      if len(row)<col: return None

      val = row[col].value

      if val is None: return None
       
      if row[col].ctype == self.XL_CELL_TEXT:
         val = codecs.encode(val,self.xlsEncoding)

      elif row[col].ctype == self.XL_CELL_EMPTY:
         val = None

      elif row[col].ctype == self.XL_CELL_BLANK:
         val = None

      elif row[col].ctype == self.XL_CELL_NUMBER:
         if str(val).split('.')[1] == '0': 
            val = int(float(val))
         else:
            val = float(val)
                  
      elif row[col].ctype == self.XL_CELL_DATE:
         from datetime import date, datetime, timedelta
         from1900to1970 = datetime(1970,1,1) - datetime(1900,1,1) + timedelta(days=2)
         val = date.fromtimestamp( int(val) * 86400) - from1900to1970
         val = str(val)

      return val      

   def doDomain(self):
      """
      Auflosen des Domain PRG Kommandos.

      Es wird dynamisch ein Domain Objekt gebildet.
      """
      sDomain = self.PRG['domain'][0]
      lstD = sDomain.split('.')
      sClass = (lstD[-1])
      dfile = '.'.join(lstD[:len(lstD)-1])
      
      c = 'from {0} import {1}'.format(dfile,sClass)
      exec(c)
      c = 'self.domain = {0}(self.db)'.format(sClass)
      exec(c)
      

   def doPRG(self,row):
      """
      Behandle Pragma (PRG) Kommando

      """
      prgname = self.getCol(row,1)

      if prgname == '': return      
      values = list()
      
      for col in range(2,len(row)):
         values.append(self.getCol(row,col))

      self.PRG[prgname]=values
     
      if prgname == 'domain': self.doDomain()
        
   def doUPD(self,row):
      """
      Veraendern eines Datensatzes.
      """
      if self.COL is None:
         raise Exception('Noch keine Spaltenkoepfe (COL) definiert')

      v = None
      c = None
      self.domain.clear()
      pkFld = self.domain.getPK()      
      
      if self.COL.count(pkFld) < 1:
         raise Exception('Bei Update muss PK Feld in COL sein.')

      self.domain.typecheckStrict = self.typecheckStrict

      for col in range(1,len(row)):
         v = self.getCol(row,col)

         if v is None: continue
         try:
            c = self.COL[col-1]
         except: 
            continue

         if isinstance(v,str):
            v = self.domain.prepareValue(c,str(v))
         self.domain.set(c,v)
    
      self.domain.update(usedFields=self.COL)

      if not self.domain.isOk:
         raise Exception('Fehlermeldung: {0}'.format('<br />'.join(self.domain.errors)))


   def doINS(self,row):
      """
      Einfuegen Datensatz
      """
      if self.COL is None:
         raise Exception('Noch keine Spaltenkoepfe (COL) definiert')

      v = None
      c = None
      self.domain.clear()
      pkFld = self.domain.getPK()
      
      if self.COL.count(pkFld) < 1:
         raise Exception('Bei Update muss PK Feld in COL sein.')

      
      self.domain.typecheckStrict = self.typecheckStrict

      for col in range(1,len(row)):
         v = self.getCol(row,col)

         if v is None: continue
         try:
            c = self.COL[col-1]
         except: 
            continue
         if isinstance(v,str):
            v = self.domain.prepareValue(c,str(v))
         
         self.domain.set(c,v)
       

      self.domain.insert()

      if not self.domain.isOk:
         raise Exception('Fehlermeldung: {0}'.format('<br />'.join(self.domain.errors)))

   def doERA(self,row):
      """
      Entfernen Datensatz
      """

      if self.COL is None:
         raise Exception('Noch keine Spaltenkoepfe (COL) definiert')

      v = None
      c = None
      self.domain.clear()
      pkFld = self.domain.getPK()
      
      if self.COL.count(pkFld) < 1:
         raise Exception('Bei Update muss PK Feld in COL sein.')

      self.domain.typecheckStrict = self.typecheckStrict
      
      for col in range(1,len(row)):
         v = str(self.getCol(row,col))
         if v is None: continue
         try:
            c = self.COL[col-1]
         except: 
            continue

         v = self.domain.prepareValue(c,v)
         self.domain.set(c,v)
      self.domain.delete()
      if not self.domain.isOk:
         raise Exception('Fehlermeldung: {0}'.format('<br />'.join(self.domain.errors)))


   def doCOL(self,row):
      """
      Definition der Spaltenkoepfe
      """
      self.COL = []
      for col in range(1,len(row)):
         if (row[col].value or '') != '': self.COL.append(row[col].value)

   def doETR(self,row):
      pkFld = self.domain.getPK()
      
      if self.COL.count(pkFld) < 1:
         raise Exception('Bei ETR muss PK Feld in COL sein.')
      idFld = row[self.COL.index(pkFld)+1]
      self.domain.get(idFld)
      if self.domain.isOk:
         self.doUPD(row)
      else:
         self.doINS(row)
      
   
   def doIFN(self,row):
      self.INF = self.getCol(row,1)

   def doREM(self,row):
      return
      

   def doLine(self,row):
      """
      Verarbeiten einer Zeile
      """
      self.comd = self.getCol(row,0)

      if self.comd      == 'IFN': self.doIFN(row)
      elif self.comd    == 'REM': self.doREM(row)
      elif self.comd    == 'PRG': self.doPRG(row)
      elif self.comd    == 'COL': self.doCOL(row)
      elif self.comd    == 'UPD': self.doUPD(row)
      elif self.comd    == 'INS': self.doINS(row)
      elif self.comd    == 'ERA': self.doERA(row)
      elif self.comd    == 'ETR': self.doETR(row)
      else:
         raise Exception ('Ungueltiges Kommando "{0}" <br />'.format(self.comd))


class XdemDomainExportBase(object):
   """
   xDem ist eine allgemeine Spezifikation zum schreiben und lesen von Dateninhalten.

   Dieses Klasse exportier den Inhalt einer Datenbanktabelle basierend auf einer Domain.

   """
   domain         = None
   exFile         = None
   fieldDelimeter = '\t'
   dbflds         = []
   domainFields   = []
   excludeFields  = []
   where          = None
   orderby        = None

   def __init__ (self,domain=None,exFile=None):
      self.domain = domain
      self.exFile = exFile
      for fld in self.domain.meta['fields'].keys():
         if not fld in self.excludeFields:
            dbfld = self.domain.getDbFieldName(str(fld))
            self.dbflds.append(dbfld)
            self.domainFields.append(fld)
      

   def __del__ (self):
      if self.exFile is not None: self.exFile.close()

   def getData (self):
      """
      Datenbankstrom auf Daeten
      """
      for domain in self.domain.eachDomain(where=self.where,orderby=self.orderby):
         yield (domain)

   def writeLine(self,values):
      """
      Gibt eine Zeile aus.
      """
      print>>self.exFile,self.fieldDelimeter.join(values)

   def writeHeader (self):
      self.writeLine(('IFN','xDEMDomain'))
      self.writeLine(('REM','Date',time.strftime('%Y-%m-%dT%H:%M')))
      self.writeLine(('REM',"excluded fields","{0}".format(', '.join(self.excludeFields))))
      self.writeLine(('PRG',"dbtype","{0}".format(self.domain.db.dbtype)))
      self.writeLine(('PRG',"table","{0}".format(self.domain.meta['tablename'])))
      self.writeLine(('PRG',"domain","{0}".format(self.domain.__class__)))

      self.writeLine(["COL"]+self.domainFields)


   def importxdem(self):
      pass

   def export (self):
      """
      Exportroutine

      HINT:
         Fuer jedes gelesenen Feld wird onField aufgerufen

      """
      self.writeHeader()      
      cnt=0

      for row in self.getData():
         values = ['UPD']
         for fld in self.domainFields:
            value = self.onField(fld,self.domain.getValue(fld)) or ''
            value = str(value)
            value = value.replace('\r','')
            value = value.replace('\n',r'\n')
            value = value.replace('\t',r'\t')
            if not fld in self.excludeFields:
               values.append(value)
         cnt+=1
         try:
            self.writeLine(values)
         except Exception,ex:
            raise Exception(ex)
            

      try:
         self.writeLine(["REM","{0} Records".format(cnt)])
      except: pass

   def onField (self,fld,value):
      """
      Wird bei jedem Feld aufgerufen
      @param   fld         Feldname (Datenbank)
      @param   value       Wert des gelesenen Feldes

      @return  ggf. veraenderter Wert des Feldes
      """
      return value

   def close(self):
      self.__del__()

   def getFileHandle (self):
      return self.exFile


if __name__ == '__main__':
   import sys
   import os
   cwd = os.getcwd()

   sys.path.extend(['.','../','../mvc/','../../'])
   from dbaccess.core import *
   db = Database('sqlite','../datastore/database/database.db3')
   from domain.taskdomain import TaskDomain
   domain = TaskDomain(db)

   xdem = XdemDomainExportBase(employees,open('c:/temp/xdem.xdem','wb'))

   #xdem.where = "LastName = 'King'"
   xdem.orderby = 'tskName'
   #xdem.excludeFields = ['Photo']
   xdem.export()
   f = xdem.getFileHandle()
   xdem.close()