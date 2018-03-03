# -*- coding: iso-8859-15 -*-
from configbase import ConfigBase
import os

# ### KONFIGURATION
# In dieser Klasse werden 
# Anwendungsspezifische Daten gesetzt
#
# HINT:
#   Erbt die frameworkspezifischen
#   Konstanten von der Klasse /mframe/ConfigBase
#
class Config(ConfigBase):
   # OS-Pfad auf das Wurzelverzeichnis der Anwendung
   cwd = os.getcwd()

   # Pfad auf Logdatein
   logfile = cwd+'/../WEB-INF/datastore/log/log.dat'

   # Dateipfade
   mvcpath           = cwd+'/../WEB-INF/mvc'
   templatepath      = cwd+'/../WEB-INF/templates'
   sessionpath       = cwd+'/../WEB-INF/datastore/session'

   # Datenbank
   sqlitefilename    = cwd+'/../WEB-INF/datastore/database/database.db3'
   
   attachmentbase    = cwd+'/../WEB-INF/datastore/attachments'
   sideboxpath       = cwd+'/../WEB-INF/sidebox'
   maintainscripts   = cwd+'/../WEB-INF/maintainscripts'
   homeurl           = 'start.py'

   # Autentifizierung
   # 
   # Beschreibt die Vorganben fuer die Verschluesselunge von Passwoerten
   # 
   # Method:      md5 
   #              pbkdf2
   #
   # Salt         Standard Saltwert
   #
   authenMethod   = 'pbkdf2'
   authenSalt     = '3a7100f48b9e4156b369d265175a1fe1'
   