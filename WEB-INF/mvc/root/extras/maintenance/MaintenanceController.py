# -*- coding: iso-8859-15 -*-
"""
Dieser Controller wird vom Framework aufgerufen.

Er ist fuer ein GRID Layout optimiert.

"""
from controller         import Controller
from helper.utility     import Utility
import os
class MaintenanceController(Controller):


   def runScript(self):
      self.showKriterien()
      sPath = self.main.config.maintainscripts+'/'+self.cgiparam('filename')
      fBuffer = open(sPath).read()
      try:
         exec(fBuffer)
      except Exception,e:
         self.render('Fehler im Skript<br />{0}'.format(e))
      self.render('<p>done</p>')


   def showKriterien(self):
      notesdir = self.main.config.maintainscripts
      
      lstFiles = []
      for files in os.listdir(notesdir):
         if files == '__init__.py': continue
         if not files.endswith('.py'): continue
         lstFiles.append(files)
      self.view('kriterien.tpl',{
         'files':lstFiles
         })
   
   
   def get(self):   
      action = self.cgiparam('action')
      if action == 'run':
         self.runScript()
      else:
         self.showKriterien()
