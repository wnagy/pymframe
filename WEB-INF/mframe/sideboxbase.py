# -*- coding: iso-8859-15 -*-

#
# Basisklasse fuer Sideboxes
# 
# Eine Sidebox stellt eine Moeglichkeit dar
# eine Menge von Bildschirmbereiche dynamisch zu gestallten.
# 
# Um Sideboxes zu kontrollieren kann eine Backlink Prozedure notiert werden.
# 
# Diese Prozedure erhaellt als Parameter
#    + self
#    + buffer
#    + file
#    + filepath
# Liefert die Procedure eine leere String zurueck
# wird die Siedebox nicht angezeigt.
#
from conf.config import Config
import os
import sys

class SideboxBase(object):


   config = None
   
   backling = None

   def __init__(self,config=None):
      if config is None:
         self.config = config
      else:
         self.config = Config()




   def getSideboxText(self,filepath):
      f = open(filepath,'r')
      buffer = f.read()
      f.close()
      return buffer

   #
   # Durchsuchen des Sideboxex Verzeichnis
   # Wird dies nicht gefunden, wird nichts zurueckgegeben
   #
   def get(self):
      """
      liefert eine Liste von Sideboxfilenamen inklusieve path alle Sideboxfiles
      """

      myPath = self.config.sideboxpath
      
      lstFile = []
      retval = ''
      try:
         for file in os.listdir(myPath):
            lstFile.append(file)
      except:
         pass

      lstFile.sort()
      
      for file in lstFile:
         filepath = myPath+'/'+file
         if not os.path.isdir(filepath):
            buffer = self.getSideboxText(filepath)
            if self.backlink is not None:
               buffer = self.backlink(self,buffer,file,filepath)

            if buffer != '':
               retval = retval + self.config.sideboxtemplate % {'text':buffer}
               
      return retval
