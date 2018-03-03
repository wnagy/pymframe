# -*- coding: iso-8859-15 -*-
import tempfile
import codecs
import sys

from xlwt               import *
from sender             import Sender
from dateconverter      import Dateconverter

from controller         import Controller
from viewhandler        import Viewhandler
from helper.utility     import Utility


from domain.gruppedomain   import GruppeDomain
from domain.persondomain   import PersonDomain

class PersonenAbfrageController(Controller):

   def insertList(self,sheet,xlsRow,lst):
      xlsCol = 0
      for f in lst:
         self.sheet.write(xlsRow,xlsCol,str(f)); xlsCol+=1


   def export(self):
      workbook    = None
      sheet       = None
      gruppe      = GruppeDomain(db=self.db)
      personen    = PersonDomain(db=self.db)
      
      xlsRow=0
      xlsCol=0

      dc = Dateconverter()
      
      xlsFile = tempfile.NamedTemporaryFile(delete=False,prefix='export-personen')
      xlsFileName = xlsFile.name
      xlsFile.close()

      self.workbook = Workbook(encoding='UTF-8')
      self.sheet = self.workbook.add_sheet('Data')

      self.insertList(sheet,xlsRow,['Auswertung vom: {0}'.format(dc.giveAsGermanDateTime('now'))])
      xlsRow+=1

      auxFilter = self.cgiparam('_filter')

      _filter = Utility.normalizeFilter(auxFilter)
      where = '(1=1)'
      if _filter.startswith('id:'):
         where = "perID={0}".format(_filter[3:])
      elif _filter.startswith('tn:'):
         where = "perArt like '%-{0}'".format(_filter[3:])
      elif _filter.startswith('bvkey:'):
         where = "perBVKey='{0}'".format(_filter[6:])
      elif _filter == '%':
         pass
      else:
         where = "lower(perNachname) like lower('%{0}%') or lower(perVorname) like lower('%{0}%')".format(_filter)

      if self.cgiparam('_perStatus'):
         where += " AND perStatus='{0}'".format(self.cgiparam('_perStatus'))

      if self.cgiparam('_perArt'):
         where += " AND perArt='{0}'".format(self.cgiparam('_perArt'))
            
      if self.cgiparam('_grpID'):
         where += " AND grpID='{0}'".format(self.cgiparam('_grpID'))
      
      self.insertList(sheet,xlsRow,[
         'ID',
         'Vorname',
         'Nachname',
         'Gender',
         'Kl.Gruppe',
         'Status',
         'Art',
         'Verpflegung',
         'EMail',
         'Telefon'
         ])
      xlsRow+=1
      
      for person in personen.eachDomain(where=where):
         gruppe.get(person.grpID or 0)

         self.insertList(sheet,xlsRow,[
            person.perID,
            person.perVorname,
            person.perNachname,
            person.perGender,
            person.kgrKennung,
            person.perStatus,
            person.perArt,
            person.perVerpflegung,
            person.perEMail or '',
            person.perTelefon or ''
            ])
         xlsRow+=1

      try:
         self.workbook.save(xlsFileName)
      except Exception,e:
         raise Exception(e)

      sender = Sender()      
      sender.sendfile(xlsFileName,'personen-export-{0}.xls'.format(dc.giveAsANSIDateTime('now')),delete=True)

   def get(self):
      self.view('kriterien.tpl')

      action = self.cgiparam('action','')

      if action == 'run':
         self.render("Starte Auswertung ...")
         self.export()
