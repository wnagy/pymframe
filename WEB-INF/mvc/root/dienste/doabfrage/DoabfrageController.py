# -*- coding: iso-8859-15 -*-
"""
Dieser Controller wird vom Framework aufgerufen.

Er ist fuer ein GRID Layout optimiert.

"""
import sqlite3
import tempfile
import codecs
import sys


from xlwt               import *
from sender             import Sender
from dateconverter      import Dateconverter
from controller         import Controller
from helper.utility     import Utility
from conf.taglib        import Taglib

from domain.abfragedomain import AbfrageDomain


class DoabfrageController(Controller):

   workbook    = None
   sheet       = None
   userRights  = None 


   def doQuery(self,abfrage):
      """
      Erzeuge Abfrage
      
      @param   abfrage        Abfrage Port

      """
      lst = abfrage.abfSql.split('\n')
      promtps = list()

      prompts = [l for l in lst if l.startswith('-- prompt ')]

      self.view('showprompts.tpl',{
         'prompts':prompts,
         'abfrage':abfrage
         }
         )
      self.doExport('screen',abfrage)

   def doExportXls(self,abfrage,sql):
      """
      Liefert die exportieren Daten als MS Excel.

      @param   abfrage        Abfrage Objekt
      @param   sql            SQL Anweisung
                              HINT: um Macros bereinigt

      """
      c = self.db.cursorFactory()
      c.row_factory = sqlite3.Row

      xlsRow=0
      xlsCol=0
      dc = Dateconverter()

      def Latin1ToUtf8(self,value):
         if value is None: return None
         try:
            return value.decode('latin1').encode('utf8')  
         except:
            return value

      xlsFile = tempfile.NamedTemporaryFile(delete=False,prefix='export-{0}'.format(abfrage.abfID))
      xlsFileName = xlsFile.name
      xlsFile.close()

      self.workbook = Workbook(encoding='UTF-8')
      self.sheet = self.workbook.add_sheet('Data')

      self.sheet.write(xlsRow,0,'Auswertung: {0} vom: {1}'.format(abfrage.abfName,dc.giveAsGermanDateTime('now')))
      xlsRow+=1

      cnt = 0
      for row in c.execute(sql):
         cnt += 1
         xlsCol=0
         if cnt == 1:
            colHeader = row.keys()
            for colh in colHeader:
               self.sheet.write(xlsRow,xlsCol,colh)
               xlsCol+=1
         xlsCol=0
         xlsRow+=1
         for v in row:
            self.sheet.write(xlsRow,xlsCol,v)
            xlsCol+=1

      try:
         self.workbook.save(xlsFileName)
      except Exception,e:
         raise Exception(e)

      sender = Sender()      
      sender.sendfile(xlsFileName,'{0}-export-{1}.xls'.format(abfrage.abfName,dc.giveAsANSIDateTime('now')),delete=True)

   def doExport(self,mode,abfrage):
      """
      Export Routine
      HINT:
         Wenn die Abfrage Promptanweisunge enhaelt und diese
         noch nicht behandelt wurden. Gibe Abfragemaske aus.

      @param      mode        xls/screen
      @param      abfrage     Abfrage Objekt

      """
      if not abfrage.checkRights(self.userRights):
         self.flash('Sie haben nicht das Recht diese Abfrage auszuf&uuml;hren!')
         return
      
      taglib = Taglib()
      sql = abfrage.abfSql.strip()
      lstLn = [l for l in sql.split('\n') if not l.startswith('--')]
      sql = ' '.join(lstLn)

      lstPrompts = self.cgiparam('lstPrompts')
       
      if lstPrompts != '':
         lstNames = lstPrompts.split(',')
         self.render('<h2>Parameter</h2>')
         for n in lstNames:
            val = self.cgiparam(n)
            val = val.replace('*','%')
            self.render ('<br />{0}={1}'.format(n,val))
            sql = sql.replace(n,val)
         self.render('<hr />')


      if not sql.lower().startswith('select '):
         raise Exception('{0} ist kein g&uuml;ltiges SQL Select Statment'.format(sql))

      if mode == 'xls':
         self.doExportXls(abfrage,sql)
         return

      c = self.db.cursorFactory()
      c.row_factory = sqlite3.Row

      cnt = 0
      for row in c.execute(sql):
         cnt += 1
         if cnt == 1:
            colHeader = row.keys()+['&nbsp']
            self.render(taglib.table(colgroup=len(colHeader)))
            self.render(taglib.tablehead(colHeader))
         self.render(taglib.tablerow([v or '~' for v in row]+[' ']))
      self.render('</table>')
      self.render('<p>{0} rows</p>'.format(cnt))
      #self.render('<p>{0}<p>'.format(sql))       

   def getAbfrage(self):
      """
      Liefert eine Abfrageobjekt
      oder None wennn keine Abfragenummer
      vorhanden.

      """
      abfID = self.cgiparam('_abfID')
      if abfID is None: return None

      abfrage = AbfrageDomain(self.db)
      abfrage.get(abfID)
      return abfrage
      

   def makeExport(self):
      """
      Erzeugen des Exports
      """
 
      action   = self.cgiparam('action')
      mode     = self.cgiparam('mode')
      abfragen = self.getAbfrage()

      if action == '':
         self.view('kriterien.tpl',{
            'abfrage':abfragen,
            'userRights':self.userRights
            }
            )

      elif action == 'start':
         if abfragen.abfSql.startswith('-- prompt '):
            self.doQuery(abfragen)
         else:
            self.render('Abfrage ID: {0} <h2>{1}</h2>'.format(abfragen.abfID,abfragen.abfName))
            self.doExport(mode,abfragen)
      elif action == 'query':
         self.doExport(mode,abfragen)         
      else:
         self.render('eine bislang unbekannte action "{0}" stellt sich vor'.format(action))



   def get(self):
      """
      Fuehrt Abfrage aus.
      Gibt Meldung aus, wenn Fehler aufgetreten is.
      """
      self.userRights = self.controller.session.getAttribute('rights')
      try:
         self.makeExport()
      except Exception,ex:
         self.render('<h2 style="color:red;">Fehler in Abfrage</h2>{0}'.format(ex))