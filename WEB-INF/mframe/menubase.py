# -*- coding: iso-8859-15 -*-
import sys
import os

from conf.config import Config

"""
 Abstrakte Klasse fuer die Menudarstellung
 Sie wird normalerweise von der Klasse Menu im WEB-INF/conf/menu
 importiert.
"""

class MenuBase:

   # ### GLOBALS
   #

   authen = None
   config = None

   # Container fuer Menuedarstellung
   tplMenuContainer     = None
   tplMenuEntry         = None
   tplMenuBullet        = None

   # Container fuer Backlink Darstellung
   tplBacklinkContainer = None
   tplBacklinkEntry     = None
   tplBacklinkSep       = None

   returnPath = ''

   # URL auf HOME, wird zum
   # erzeugen des URL mit Path verwendet
   # meist 'start.py'
   #
   homeurl=None

   # aktueller Inhalt des CGI Parameters path
   # wird von main.py gesetzt
   path=None

   # Menueintraege
   # HINT:
   #   Wird von der Klasse menu
   #   im Verzeichnis conf bei der Initialisierung gesetzt
   #
   entries = []
   addentries = []

   #
   # Konstante fuer URL Kennung in Controller
   #
   controllerIsUrl = '@url:'

   error = ''

   def writelog(self,*args):
      print >>sys.stderr,' '.join([str(a) for a in args])

   def __init__(self,config=None):
      if config == None:
         self.config = Config()
      else:
         self.config = config

      
      self.tplMenuContainer     = self.config.tplMenuContainer
      self.tplMenuEntry         = self.config.tplMenuEntry
      self.tplMenuBullet        = self.config.tplMenuBullet

      # Container fuer Backlink Darstellung
      self.tplBacklinkContainer = self.config.tplBacklinkContainer
      self.tplBacklinkEntry     = self.config.tplBacklinkEntry
      self.tplBacklinkSep       = self.config.tplBacklinkSep

      # Text des Zurueck Buttons
      self.returnText = self.config.returnText


   
   def getEntry(self,path,dieifnotfound=True):
      '''Gibt ein Entry referenziert auf path zurueck
         Wenn "dieifnotfound" gesetzt ist
            wirft Exception wenn nicht auffindbar
         sonst
            wird None zurueckgegeben
         '''
      # durchlaufen der Menueeintraege
      #
      for entry in self.entries:
         # Wenn Eintrag gefunden, wird
         # das Dictionary zurueckgegeben
         if entry['path'] == path:
            return entry
      # Wurde der Parameteär dieifnotfound
      # gesetzt wird, wenn der Eintrag nicht
      # gefunden wurde eine Exception geworfen
      if dieifnotfound:
         return None
         raise Exception("Kann keinen Einrag basierend auf '%(path)s' finden" % {path:path})

      # Wenn nicht gefunden, None zurueckgeben
      return None


   def truncatepath(self,path):
      'Abschneiden des letzen Teils des Pfades'

      # Wenn kein Pfad definiert
      # abbruch
      if path is None:
         return

      # Finde den letzten Pfadtrenner
      pos = path.rfind('/')

      # wurde dieser nicht gefunden,
      # wird ein Leerstring zurueckgeliefert
      if pos == -1:
         return ''

      # ist nur mehr ein Eintrag vorhanden
      # diesen Zurueckgeben
      if pos == 0:
         return '/'

      # Wenn wir bis hierher gekommen sind
      # letzen Eintrag abschneiden und das Ergebnis
      # zurueckliefern
      return path[0:pos]

   def getHtml(self,entry):
      'Liefert das HTML Snippet fuer die Anzeige'
      
      if (entry.get('text') or '').startswith('@header:'):
         hdr = entry.get('text') or ''
         hdr = hdr.replace('@header:','')
         return '<li class="menu-hdr">{0}</li>'.format(hdr)

      
      if entry.get('text') == '@hr':
         return '<li class="menu"><hr class="menu" /></li>'

      if (entry.get('text') or '').startswith('@hint:'):
         hint = entry.get('text') or ''
         hint = hint.replace('@hint:','')
         return '<li class="menu-hint">{0}</li>'.format(hint)

      controller = entry.get('controller')

      if controller is None: controller = ''

      # Spezialbehandlung, wenn der Eintrag ein URL ist
      #
      if controller.startswith(self.controllerIsUrl):
         formatstring = self.tplMenuEntry
         controller = controller.replace(self.controllerIsUrl,'')
         formatstring = formatstring.replace('%(homeurl)s?path=%(entry)s',controller)         
         retval = formatstring % {'text':entry.get('text'),'tplMenuBullet':self.tplMenuBullet}
         return retval

      # Path
      myPath = entry.get('path') or ''         
      
      # Wurde Pfad mit '/' beendet, dieses abschneiden
      if myPath != '/' and myPath.endswith('/'): myPath = myPath.rstrip('/')
      # Behandeln von zusaetzlichen CGI Parametern
      if 'addparam' in entry:
         cntP = 0
         for param in entry['addparam']:
            myPath += "&%s" % param
      
      entryParams = {
         'homeurl':self.homeurl,
         'entry':myPath,
         'text':entry['text'],
         'tplMenuBullet':self.config.tplMenuBullet
         }
   
      # Optionale Parameter in Datenstruktur einfuegen
      if '%(id)s' in self.tplMenuEntry:
         menID = ' id="{0}" '.format(entry['text'] if not 'id' in entry else entry['id'])
         entryParams['id']= menID

      if '%(title)s' in self.tplMenuEntry:         
         entryParams['title'] =  ' title="{0}" '.format(entry['title'] if 'title' in entry else self.config.tplTitleDefault)
         
      retval = self.tplMenuEntry % entryParams

      return retval


   def hasEntryRight(self,entry):
      """
      Liefert True wenn der User das Recht hat den Menueintrag aufzurufen
      """
      if (hasattr(self.config, 'useauthen')) and (not self.config.useauthen): return True
      # Rechte des Menueeintrags
      rights = entry.get('rights')   
      return self.authen.checkRights(rights)

   def navigation(self):
      'Gibt das gesamte Menue zurueck'
      retval = ''

      # zusammenstellen Menue
      for entry in self.entries:
         # Wenn kein Texteintrag nicht anzeigen
         if entry.get('text') is not None:
            # Letzten Pfadeintrag abschneiden
            truncpath = self.truncatepath(entry['path'])
            # Im aktuellen Pfad
            if truncpath == self.path:
               # Ueberpruefen ob User berechtigt ist
               showIt = self.hasEntryRight(entry)
               # Display Attribute bearbeiten
               if showIt:
                  if 'display' in entry:
                     showIt = entry['display']

               if showIt:
                  retval = retval + self.getHtml(entry)

      # Zusaetzliche Entries werden bearbeited
      for entry in self.addentries:
         showIt = self.hasEntryRight(entry)
         if showIt:
            retval = retval + self.getHtml(entry)


      # Wenn nicht oberste Ebene
      # wird Return Schaltflaeche ausgegeben
      # wenn returnText angegeben.

      if self.path != '/root':
         if self.returnPath == '':
            self.returnPath = self.path

         if self.returnText is not None:
            retval = retval + self.getHtml({'path':self.truncatepath(self.returnPath),'text':self.returnText})
      return self.tplMenuContainer % {'entry':retval}

   def backlink(self):
      retval = ''

      path = self.path  #self.truncatepath(path=self.path)
      while (path != '/'):
         entry = self.getEntry(path)
         # Ueberpruefen der Option display [True|False]
         # ist display False wird der Eintrag nicht angezegt
         if entry is not None:
            display = True if entry.get('display') is None else entry.get('display')
         else:
            display = False
         if not display:
            path = self.truncatepath(path)
            continue

         if entry==None:
            text = ''
         else:
            text = entry.get('text')

         if text is not None:
            url = self.tplBacklinkEntry % {'root':self.config.homeurl,
                                           'path':path,
                                           'text':text
                                           }

            # Bei aktuellem Pfad keinen Trenner einfuegen
            if path != self.path:
               url += self.tplBacklinkSep
            # Resultat zusammenbauen
            retval = url + retval

         path = self.truncatepath(path)

      # moeglicherweise vorhandener leeren Seperator entfernen
      retval = retval.rstrip(self.tplBacklinkSep)

      return self.tplBacklinkContainer % {'entry':retval}

   def setDisplay(self,path=None,mode=True):
      """
      Setzt den Display Status des Eintrag
      @param   path        Patheintrag
      """

      entry = self.getEntry(path,dieifnotfound=True)
      entry['display'] = mode

   def setText(self,path=None,text=''):
      """
      Setzt den Display Status des Eintrag
      @param   path        Patheintrag
      @param   text        Text
      """

      entry = self.getEntry(path,dieifnotfound=True)
      entry['text'] = text

   
   def setParam(self,path=None,param=[]):
      """
      Setze dynamisch zusaetzliche Parameter in Menueeintrag
      @param   path        Patheintrag
      @param   param       Paramter als Liste.
      """

      entry = self.getEntry(path,dieifnotfound=True)
      entry['addparam'] = param

   
   def setController(self,path=None,controller=''):
      """
      Setzt den Controleraufruf
      @param   path        Patheintrag
      @param   controller  controller
      """

      entry = self.getEntry(path,dieifnotfound=True)
      entry['controller'] = controller
      
   def getControllerPath(self):
      """
      Liefert eine relativen Pfad auf einen Controller.
      Wird nur der Namen angeben, so wird dieser aus der Pfad Option
      und dem Controllernamen des Menueeintrags gebildet.

      Beginnt der Controller Eintrag mit '/' so wird der Pfad relativ zu WEB-INF gebildet.
      """
      entry = self.getEntry(self.path,dieifnotfound=False)
      if entry is None:
         entry = {}
      
      if 'controller' in entry:
         sController = entry['controller']
         if sController.startswith('/'):
            sController = sController.lstrip('/')
            auxPath = sController            
            return auxPath

         elif sController.startswith('file://'):
            auxPath = sController[7:]            
            return auxPath            
         else:
            auxPath = self.path
            auxPath = auxPath.replace('/','.')
            retval = "mvc%(path)s.%(controllername)s" % {'path':auxPath,'controllername':entry.get('controller')}
            
            return (retval)
      else:
         return None

   def getControllerName(self):
      """
      Behandelt die Verwendung von relativen Pfadangaben im Controller Eintrag

      Liefert den Dateinamen des Controllers ohne ".py"

      HINT:
         Verwendet zur Bildung des Namens os.path

      """
      sControllerPath = self.getControllerPath()
      sControllerPath = sControllerPath.replace('.','/')
      (path,tail) = os.path.split(sControllerPath)
      return tail


   def getController(self):
      '''Liefert eine Controller Objekt
         Es wird angenommen, dass der Controller im Dateisystem
         mit dem Pfad der CGI variable path liegt.

         Desweiteren wird ueberprueft, ob der Benutzer das Recht hat
         diesen Controller aufzurufen.
         '''

      self.error = ''

      entry = self.getEntry(self.path)

      if entry is None:
         raise NameError
         

      if 'controller' in entry:
         if entry.get('controller') is None:
            return None

         if entry.get('controller').startswith('@url:'):
            return None

         
         if not self.hasEntryRight(entry):
            raise ValueError

         cpath = self.path.replace('/','.')
         # vorlaufender Punkt entfernen
         cpath = cpath.lstrip('.')

         # Prepare controllername
         sControllerPath = self.getControllerPath().replace('/','.')
         sControllerName = self.getControllerName()

         sImport = "from %(from)s import %(import)s as Controller" % {
            'from':sControllerPath,
            'import':sControllerName
            }
         errormsg = None

         try:
            exec (sImport)
         except Exception,e:
            errormsg = '<b>Error: '+str(e)+'</b>'

         if errormsg is not None:
            raise(Exception('<br /><span style="color:darkblue;font-size:larger;">'+sImport+'</span><br />kann nicht ausgefuehrt werden.<br />'+errormsg))

         controller = Controller()
         controller.path=self.path
         return controller
      else :
         return None
