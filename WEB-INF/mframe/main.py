# -*- coding: iso-8859-15 -*-
"""
Diese Klasse ist die Hauptsteuerroutine des Frameworks.

Sie steuert das gesamte Verhalten.
Es werden die Subklassen instanziert

"""
import cgi
import os
import sys
import traceback

from urlparse           import *
from cgi                import FieldStorage
from cgi                import MiniFieldStorage
from conf.menu          import Menu
from conf.config        import Config
from conf.authen        import Authen
from conf.sidebox       import Sidebox
from templateengine     import TemplateEngine
from dbaccess.core      import *
from session            import Session
from version            import Version


# ### Hauptklasse des Frameworks
#
class Mframe:
   form=None                                    # aktuelle Form (gesetzt aus CGI)
   webini=None                                  # Pfad auf Standard Hilfsverzeichnis WEB-INF
   menu=None                                    # Menu Objekt
   homeurl='start.py'                           # HOME URL
   path=None                                    # Aktueller Pfad gesetzt aus der CGI Variabel path
   db=None                                      # Databasehandle
   session=None                                 # Session Objekt
   authen=None                                  # Autentifizierungsmodul
   container=Config.defaulttemplate             # Standard Template aus Config
   tplateengine = None                          # Template Engine
   flash=''                                     # Meldungszeile
   useAuthen = True                             # Flag zur Benutzung der Autentifizierung
   sidebox = None                               # Sideboxbearbeitung
   config = None                                # Konfigurationsobjekt
   showSideboxes = False                        # True wenn Sideboxes angezeigt werden sollen
   sideboxes = ''                               # Container haelt Sideboxes HTML Snippet
   version = None                               # Versionsinformationen
   mframeversion = None                         # Versionsnummer von mFrame
   logintemplate=Config.defaultlogintemplate    # Standard Logintemplate
   templateparam = {}                           # Dictionary fuer Template
   javascript = ''                              # Standard Javascript
   stylesheet = ''                              # Stylesheet
   query_string = ''                            # Query String vom CGI

   
   defaultMimeHeader = "Content-Type: text/html"

   def __init__(self,webini='../../WEB-INF',sessionlifetime=180,usecgi=True):
      """
      Konstruktor:

      @param   webini            Pfad auf WEB-INI Verzeichnis
      @param   sessionlifetime   Minuten welche die Session gueltig ist
      @param   usecgi            True:  es wird die cgi Classe fuer das Interfacehandling benutzt
                                 False: es wurd nur der QUERY_STRING geparst
                                 Das Standardverhalten ist usecgi=True.
      """
      self.usecgi = usecgi

      self.config = Config()
      
      # lese path aus CGI
      self.query_string = os.environ['QUERY_STRING']
      self.path = self.getPathFromQueryString()
      
      # Konfiguration
      self.homeurl=self.config.homeurl
      self.webini=webini
      self.menu=Menu(self.config)
      self.configMenu()
      self.sidebox = Sidebox(config=self.config)
      self.session = Session(self.config.sessionpath,sessionlifetime=sessionlifetime)
      self.mframeversion = Version().VERSION
      self.version = '0.1-E001'
      self.connectDb()
      self.authen = Authen(session=self.session,db=self.db)
      self.menu.authen = self.authen
      self.tplateengine = TemplateEngine(self.config)      
      self.writelog("-- usecgi: {0}".format(usecgi))
      if usecgi:
         self.form=cgi.FieldStorage(keep_blank_values=1)
         self.path = self.cgiparam(name='path',nvl='/')

   @staticmethod
   def getCgiParameter(param,nvl=''):
      """
      Liefert den Inhalt eines CGI Parmeters basierend auf den QUERY_STRINGS

      @param   param    Name des CGI Parameters
      @param   nvl      Null-Value wird zurueckgeliefert, wenn der 
                        Parameter nicht vorhanden ist.
                        Vorgabewert ''

      HINT:
         Es wird nur das 1. Vorkommen des Parameters ausgewertet!

      """
      query_string = os.environ['QUERY_STRING']
      parsed = parse_qs(query_string)
      retval = parsed.get(param)
      if retval is None: 
         return None
      else:
         return retval[0]
   
   def loadCgiParameter(self):
      """
      Laed den Inhalt des CGI in Abhaengigkeit des Flags usecgi.

      usecgi
         True:    Es wird die Lib cgi verwendet
         False:   Es wird QUERY_STRING verwendet

      HINT:
         In bestimmten Situationen z.B. wenn im HTTP Body nur daten uebertragen werden.
         verhaelt sich das CGI Modul so, dass es einen Ausnahmebedingung wirft.
         Der Flag usecgi ermoeglicht das Abschalten des Moduls. Die CGI Parameter werden
         aus dem URL extrahiert und so verspeichert, dass sie mit der Methode cgiparam 
         wiedergewonnen werden koennen.

      """
      if self.usecgi:
         self.form=cgi.FieldStorage(keep_blank_values=1)
         self.path = self.cgiparam(name='path',nvl='/')
      else:
         # Form inhalte holen
         qs = self.query_string

         parsed = parse_qs(qs)
         self.writelog ("-- QUERY_STRING: {0}".format(qs))
         self.writelog ("-- Parsed:")

         self.form = dict()

         for key in parsed.keys():
            for val in parsed.get(key):
               self.writelog("    {0} -> {1}".format(key,val))
               self.form[key] = val
         try:
             self.path=parsed.get('path')[0]
         except: 
            self.form = {'path':'/root'}
                  
         self.path = self.cgiparam('path','/root')
      
         self.writelog("-- path (cgiparam): {0}".format(self.cgiparam('path')))

   def getParsedQueryString(self):
      """
      Liefert den geparsten Query String
      """
      return cgi.parse_qs(self.query_string)


   def getPathFromQueryString(self):
      """
      Liefert aus dem Query String den Path eintrag.

      HINT:
         Wenn nicht gefunden, wird None zurueckgeliefert
      """
      qs = self.getParsedQueryString()
      path = [''] if qs.get('path',None) is None else qs.get('path')
      return path[0]

   
   def cgiparam(self,name=None,nvl='',noneifnotused=False):
      """
      Liefert aus dem CGI einen benannten Parameter

      @param   name     Name des Cgiparmeters
      @param   nvl      NullValue wird geliefert,
                        wenn der Parameter nicht uebergeben wurde

      HINT:
         Es wird geprueft, ob self.form ein Dict oder FieldStorage ist.
         Je nach Type wird der Inhalt geliefert.

      """      
      if self.form is None:
         return nvl
      
      # Wurde Spezielle CGI Verarbeitung gewünscht
      if isinstance(self.form,dict):
         return self.form.get(name,nvl)

      # wenn Parameter nicht definiert
      # null-value zurueckgeben
      if name not in self.form:
         if noneifnotused:
            return None
         else:
            return nvl

      value = self.form.getvalue(name)
      
      if value is None:
         value = nvl
      else:
         if isinstance(value,list):                 
            try:
               value = value[0]
            except: value = nvl

      return value

   def writelog(self,*args):
      print >>sys.stderr,' '.join([str(a) for a in args])
      sys.stderr.flush()

   def connectDb(self):
      # Verbinden mit Datenbank
      # Wenn dbfilename angegeben
      if self.config.dbtype == 'sqlite':
         if self.config.sqlitefilename is not None:           
            self.db = Database('sqlite',self.config.sqlitefilename)
           
         else: pass
      elif self.config.dbtype == 'mysql':
         mysqlConn = self.config.mysql
         self.db = Database('mysql',mysqlConn['host'],mysqlConn['port'],mysqlConn['username'],mysqlConn['password'],mysqlConn['schema'])
      elif self.config.dbtype == 'oracle':
         try:
            ocrConn = self.config.oracle
         except:
            raise ValueError, "Es wurden keine ORACLE Verbindungsparameter in config deklariert (oracle : {...})"
         self.db = Database('oracle',
                            ocrConn['username'],
                            ocrConn['password'],
                            ocrConn['sid'],
                            ocrConn['host'],
                            ocrConn['port'])
      



   def setContainer(self,name=None):
      """
      Setzt den zu verwendenden Container.
      Ein Container befindet sich normalerweise als Datei
      in ./WEB-INF/temlate und stellt den aeusseren Rahmen
      in HTML dar. Er enhaelt Platzhalter in denen die Werte
      aus dem Framework eingetragen werden.

      @param   name        Name des Containerfiles

      """
      self.tplateengine.tplFileName = name

   def setAttribute(self,name=None,value=None):
      """
      Setzt ein Attribut in der Session.

      @param   name        Name des Attributes
      @param   value       Wert des Attributes

      """
      self.session.setAttribute(name,value)

   def getAttribute(self,name=None):
      """
      Liefert den Wert eines Attributes oder None
      wenn dieses nicht gefunden wurde aus der Session.

      @param      name        Attrbutname

      @return     Attributwert
      """
      return self.session.getAttribute(name)


   # depricated
   def start_html(self):
      print "<html><body>"

   # depricated
   def end_html(self):
      print "</body></html>"


   def setEntryDisplay(self,path=None,mode=True):
      """
      Setzte den Displaystatus

      @param   path        Patheintrag
      @param   mode        True/False (Vorgabewert True
      """
      self.menu.setDisplay(path,mode)


   def setEntryText(self,path=None,text=''):
      """
      Setzte den Text

      @param   path        Patheintrag
      @param   text        Texteintrag
      """
      self.menu.setText(path,text)


   def setEntryController(self,path=None,controller=''):
      """
      Setzte den Text

      @param   path        Patheintrag
      @param   contrroller Controllereintrag
      """
      self.menu.setController(path,controller)
   
   
   def setEntryParam(self,path=None,param=[]):
      """
      Setzte zusaetzliche Parameter in Entry

      @param   path        Patheintrag
      @param   param       Zusaetzliche Parameter als Liste
      """
      self.menu.setParam(path,param)


   def addEntry(self,
               path='/',
               controller=None,
               text=None,
               addparam=None
               ):

      """
      Fuegt in die Menueeintraege einen Eintrag dynamisch hinzu

      @param   path        Der Path unter dem der Eintrag eingetragen
                           werden soll
      @param   controller  Controller Name
                           Beginnt der Controller name mit "@url:"
                           wird ein Link mit dem Inhalt nach @url: erzeugt
      @param   text        Anzeigetext (darf nicht leer sein da sonst keine
                           Anzeige erfogt.

      @param   addparam    eine Liste mit Parameter, welche dem
                           Link hinzugefuegt werden. z.B. ['action=list-edit']
      """

      myPath = path
      if myPath == '@current':
         myPath = self.path

      if not myPath.endswith ('/'): myPath = myPath + '/'
      aux = {}
      aux['text']=text
      aux['path']=myPath
      if controller is not None: aux['controller']=controller
      if addparam is not None:
         aux['addparam'] = addparam
      else:
         aux['addparam'] = []

      self.menu.addentries.append(aux)

   def configMenu(self,container=None,entry=None):
      """
      Liefert ein gerendetes Menue

      Konfigurieren des Menues:
       @param container      Ein Container in dem die Menueeintraege
                             eingefuegt werden
                             Beispiel: '<ul>{0}</ul>'
       @param entry          Ein Format fuer einen Menueeintrag
                             'Beispiel: <a href={0}?path={1}>{2}</a><br />'
                             Parameter:
                                0   URL
                                1   aktueller Pfad
                                2   Anzeigetext

      """

      if container is None:
         container = '<ul class="menu">\n%(entry)s</ul>\n'

      self.menu.tplMenuContainer       = container
      if entry is not None:
         self.menu.tplMenuEntry        = entry

   def reload(self,path):
      """"
      Liefert einen http-equiv Fuer in Browserreload

      @param   path        Pfadeintrag
      @return  gerenderte Eintrag
      """      
      retval = 'meta http-equiv="refresh" content="0;url="{url}">'.format(url=path)
      
      return retval

   def redirect(self,path,other=None):
      """
      Liefert einen Redirect mittels Statuscode 303 (moved permantly)

      HINT:
         gibt immer False zurueck um einfacher in einem Controller
         verwendet werden zu koennen.

      @param   path        Pfad
      @param   other       weiter CGI Parameter (optional)
      """

      moreparam = '&'+other if other is not None  else ''

      #raise Exception("Refresh: 0; url={0}?path={1}{2}".format(self.config.homeurl,path,moreparam))
      print "Refresh: 0; url={0}?path={1}{2}".format(self.config.homeurl,path,moreparam)
      return True


   def reloadmask(self,msg=''):
      lstUrl = list()
      for fld in self.form.keys():
         val = self.form.getfirst(fld)
         if isinstance(val,list):
            for v in val:
               lstUrl.append('{key}={val}'.format(key=fld,val=v))
         else:
            lstUrl.append('{key}={val}'.format(key=fld,val=val))

      return '&'.join(lstUrl)

   def init(self):
      """
      Initaialsierungsroutine des Frameworks

      HINT:
         Prueft ob der Benutzer eingelogt ist
         Ist dies nicht der Fall, wird die Einloggmaske verwendet

      """
      
      self.menu.path = self.path
      self.menu.homeurl=self.homeurl
      
      if self.useAuthen:
         # Ist noch niemand angemeldet
         if not self.authen.isAuthenticated():
            self.setContainer(name=self.logintemplate)
            self.tplateengine.readTemplateFile()

   def appException(self,controllerfilename,message):
       """
       Ausgabe der Standard Fehlermeldung

       @param  controllerfilename      Name des Controllers
       @param  message                 Nachrichtentext
       """
       return """Content-Type: text/html\n\n
                 <html><body>
                 <div style="border:2px solid red;font-family:Tahoma,sans-serif;padding:16px;">
                 <h1 style="background-color:red;color:white;margin:0;font-size:1em;">Hoppla...</h1>
                 <p>
                 In der Anwendung ist ein unerwartetes Ereignis aufgetreten
                 </p>
                 <p>
                 Controller: <strong>%(filename)s</strong><br />
                 </p>
                 <p>
                 Meldung:
                 <strong>%(meldung)s</strong>
                 </p>
                 <p>
                 Bitte senden sie diese Meldung an den Anwendungsgentwickler
                 </p>
                </div>
                </body></html>
                """ % {
                   'filename':controllerfilename,
                   'meldung':message
                   }

   # Setzten des Flashparameters
   def setFlash(self,msg):
      """
      Setzen des Nachrichtentextes auf der Maske

      @param   msg         Nachrichtentext
      """
      self.flash = msg

   def run(self):
      """
      Starten des Frameworks

      Setzt die delegierten Klassen und ruft den
      Controller auf, welcher in der CGI Variabe path
      enthalten ist.
      Der Rueckgabewert des Controllers wird in das
      Template integriert.
      Der gesamte HTML Text wird an den Browser gesendet.

      """

      menu=self.menu.navigation()
      backlink=self.menu.backlink()
      
      controllerfilename=self.menu.getControllerPath()
      
      hasError = False
      content = ''
      controller = None
      self.entry = []
      # Wenn rights in Eintrag vorhanden diese aus dem Eintrag holen

      myEntry = self.menu.getEntry(self.path)
      if myEntry is not None and 'rights' in myEntry:
         self.entry = self.menu.getEntry(self.path)['rights']


      # Controller ermitteln
      try:
         controller = self.menu.getController()

      # Berechtigungsfehler
      except ValueError: 
         # Nur Meldung anzeigen, wenn Benutzer angemeldet
         if self.authen.isAuthenticated():
            self.flash = "Sie haben nicht die Berechtigung f&uuml;r '{0}'".format(self.path)

      # Fehlerhafter Controller Pfad
      except NameError:
         if self.path != '/':
            self.flash = "Kein Controller '{0}' gefunden!".format(self.path)

      # sonstige Fehler
      except Exception, e:
         return self.appException(controllerfilename,'Filename: {0}<br />{1}<br /><p><u>Pfade:</u><br />{2}</p><p><u>Current Dir [os.getcwd()]:</u><br /> {3}</p>'.format(
            controllerfilename,
            str(e.message),
            '<br />'.join(sys.path),
             os.getcwd()
            )
          )

      
      self.main = self
      
      user = self.getAttribute('user')
      if user is None:
         user = ''

      myRights = self.session.getAttribute(name='rights')
      
      if controller is not None:
         # Controller initialisieren
         #
         controller.db                    = self.db
         controller.addEntry              = self.addEntry
         controller.setEntryDisplay       = self.setEntryDisplay
         controller.setEntryParam         = self.setEntryParam
         controller.setEntryController    = self.setEntryController
         controller.main                  = self
         controller.cgiparam              = self.cgiparam
         controller.writelog              = self.writelog
         controller.flash                 = self.setFlash
         controller.menu                  = self.menu
         controller.path                  = self.path
         controller.controllerfilename    = controllerfilename
         controller.isReadonly            = self.authen.isReadonly(self.entry)
         controller.config                = self.config
         controller.user                  = user
         controller.controller            = self
         controller.rights                = myRights

         try:
            content = controller.get()
         except Exception,e:
            return self.appException(controllerfilename,str(e.message))
         
         if content is None:
            content = controller.html
         elif content == True:
            content = controller.html
         else:
            return ''


         menu=self.menu.navigation()
         backlink=self.menu.backlink()

         if self.showSideboxes:
            self.sideboxes=self.sidebox.get()
         
      if self.flash == '':
         if self.cgiparam(name='flash',nvl='') != '':
            self.flash = self.cgiparam(name='flash',nvl='')
               

      self.stylesheet+=self.config.stylesheet
      self.javascript+=self.config.javascript
      
      theContent = self.defaultMimeHeader+'\n'+str(self.session.cookie)+'\n\n'

      # Nur flash bauen wenn vorhanden.
      tmpFlash = '' if self.flash == '' else Config.templateFlash % {'flash':self.flash}

      self.templateparam['stylesheet']=self.stylesheet
      self.templateparam['javascript']=self.javascript
      self.templateparam['body']= content
      self.templateparam['menu']=menu
      self.templateparam['flash']=tmpFlash
      self.templateparam['backlink']=backlink
      self.templateparam['sid']=self.session.getSID()
      self.templateparam['user']=user
      self.templateparam['sideboxes']=self.sideboxes
      self.templateparam['version']=self.version
      self.templateparam['path']=self.path
      self.templateparam['mframeversion']=self.mframeversion
      self.templateparam['rights']=myRights
      self.templateparam['pythonversion'] = sys.version_info

      self.tplateengine.readTemplateFile()

      theContent += self.tplateengine.get(self.templateparam)
      return theContent
