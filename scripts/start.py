#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import os
import cgitb

# ### DEBUG
# Gibt im Fehlerfall
# debugmesseages aus
# Aktiviere folgende Zeile
# fuer Debug im Apache
# print "Content-Type: text/plain\n"
#
cgitb.enable(format='text')

# ### Rootverzeichnis setzen
# Diese Sequenz ist nur notwendig,
# wenn der Python interne Webserver (CGIHTTPServer) verwendet wird.
#
if os.environ['SERVER_SOFTWARE'].find('SimpleHTTP') != -1:
   cwd = os.getcwd()

   if os.name == 'posix': # wir sind auf dem Max (OSX)
      os.chdir(cwd)
   elif os.name == 'nt': # windows
      path =cwd+'/scripts'
      os.chdir(path)

# ### Definition der Pfade auf Bibliothken
#
sys.path.extend([
   '../WEB-INF/mframe',       # Framework
   '../WEB-INF/mvc',          # Root fuer Domains
   '../WEB-INF',              # WEB-INF (Ressourcen)
   '../WEB-INF/addons',       # Zusatzmodule
   '../WEB-INF/site-packages' # Externe Zusatzmodule
   ])

# Importieren Framework
from main import Mframe

# Importiere applikationsspezifische Konfiguration
from conf.config import Config

# Initialisieren des Frameworks
mfw = Mframe()

# Authorisierungssystem verwenden
mfw.useAuthen = True

# In publicsites werden die Pfade definert,
# welche nicht durch das Autorisierungssystem
# geschuetzt werden sollen.
publicsites = ('/authen')
if mfw.cgiparam(name='path',nvl='') in publicsites:
   mfw.useAuthen = False

# Initialisierungsroutinen
mfw.init()

# Anwendungsversionsnummer
mfw.version = '1.00R007'

# Framework aufrufen
# HINT:
#   Das Framwork liefert eine
#   fertig gerenderte HTML Seite
#
print mfw.run()


'''
--Vers--+-Wer-+--Was ------------------------------------------
1.00     ny    Erstellt
'''







