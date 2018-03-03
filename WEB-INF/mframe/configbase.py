# -*- coding: iso-8859-15 -*-

class ConfigBase:
   """
   Standert Vorgabe wert fuer das Framework.

   HINT:
   Diese Klasse wird von Config der Anwendung geerbt und dort angepasst.

   $APPROOT/WEB-INF/conf/config.py

   """

   # Datenbankart
   # Folgende DB Arten werden unterstuetzt
   #  - sqlite
   #  - oracle
   dbtype = 'sqlite'

   # Verzeichnispfad auf die Templates
   templatepath               ='../../WEB-INF/templates'

   # Homeurl (wird zum Zusammenbau des URLs benoetigt
   homeurl                    ='/scripts/start.py'

   # Vorgabewert fuer Standardtemplate
   defaulttemplate            ='default.tpl'

   # Vorgabewert fuer Login Template
   defaultlogintemplate       ='login.tpl'

   # Template fuer Flash
   templateFlash              ='<div id="flash">%(flash)s</div>'

   # Pfad auf Sideboxes
   sideboxpath                ='../../datastore/sideboxes'

   # Sindboxex Container
   sideboxtemplate='''
      <div class="sidebox">
         %(text)s
      </div>
      '''

   # Zurueckbutton Text
   # HINT: ist dieser None wird kein automatischer Zurueckbutton erzeugt.
   #
   returnText = 'Zur&uuml;ck'

   # Default Styleheets
   stylesheet = '''
     <!-- default stylesheets -->
     <link rel="stylesheet" href="../css/skin/normal/normal.css" type="text/css" />
     <link rel="stylesheet" href="../css/skin/normal/add.css" type="text/css" />
     <!-- end stylesheets -->
      '''

   # Default Javascript
   javascript = '''
     <!-- default Javascript -->
     <!-- end Javascript -->
     '''

   # Menuesteuerungskonstanten
   #
   # Container fuer Menuedarstellung
   tplMenuBullet = ''
   tplMenuContainer='<ul class="menu">\n%(entry)s</ul>\n'
   tplMenuEntry=' <li class="menu" >%(tplMenuBullet)s&nbsp;<a class="menu" href="%(homeurl)s?path=%(entry)s">%(text)s</a></li>\n'
   tplTitleDefault = 'Anklicken zum Aktivieren'

   # Container fuer Backlink Darstellung
   tplBacklinkContainer = '<span style="font-size:smaller">Du bist hier: %(entry)s</span>'
   tplBacklinkEntry = '<a href="%(root)s?path=%(path)s"  class="backlink-menu">%(text)s</a>'
   tplBacklinkSep = '&nbsp;/&nbsp;'

   # Feldersetzung in database.core werden die
   # Beginn- und Endkennungen gesetzt
   # Default sind
   # Beginn mit '$' und keine Endkennung
   # Bsp: $Domainfield --> DDLFeld
   #
   SqlConverter_fieldBegin    = '$'
   SqlConverter_fieldEnd      = ''

   # Autentifizierung
   # 
   # Beschreibt die Vorganben fuer die Verschluesselunge von Passwoerten
   # 
   # Method:      md5 
   #              pbkdf2
   #
   # Salt         Standard Saltwert
   #
   authenMethod   = 'md5'
   authenSalt     = '3a7100f48b9e4156b369d265175a1fe1'
