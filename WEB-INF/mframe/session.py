# -*- coding: iso-8859-15 -*-

import os
import base64
import Cookie
import pickle
from time import *
from conf.config import Config

class Session:
   """ Sessionverwaltung:

      Die Sessinvewaltung benoetigt eine Verzeichnis
      in das die Sessionfiles geschrieben werden koennen (sessionpath)

      Dies ist eine auf Cookies basierende Sessionverwaltung. Cookies muessen im Browser erlaubt sein!
      Der Cookiname ist 'sid'.

      Die Sessions werden in Dateien verwaltet. Das Verzeichnis, in welchem die Dateien gespeichert sind
      wird in der Klassenvariable sessionpath gespeichert. Diese wird relativ zum Framework im
      Konstruktor vorbelegt.
      HINT:
         Unixoide:         Schreibrechte beachten!

      Lebenszeit der Session:
      Die Lebenszheit der Session wird in der Klassenvariable sessionlifetime gehalten.
      Die Lebenszeit wird in Minuten agegeben.

      Schreiben, lesen und loeschen von Sessinattribute:

      Wesentliche Methoden
      --------------------
        + setAttribute(name=, value=)
          zum setzen eines Attributs
        + getAttribute(name=)
          zum lesen eines Attributs
        + removeAttribute(name=)
          zum entfernen eines Attributs
   """

   sid               = ''     # Sessionid (Inhalt des Cookies)
   sessionpath       = '.'    # Pfad auf das Sessionverzeichnis
   sessionlifetime   = 180    # Lifetime der Session
   cookie            = None   # Cookie Objekt
   sHHTP_COOKIE      = ''     # Cookiestring vom Webserver
   attributes        = {}     # Attribute aus Session


   # ### Konstruktur setzen Attribute
   #
   def __init__(self,sessionpath=None,sessionlifetime=None,config=None):
      """
      Initialisieren der Session

      Pruefen ob Sessionverzeichnis vorhanden, wenn nicht anlegen.
      """
      if sessionlifetime is not None:
         self.sessionlifetime = sessionlifetime

      if sessionpath is None:
         self.sessionpath = Config.sessionpath
      else:
         self.sessionpath = sessionpath

      # legt Sessionverzeichnis an, wenn nicht vorhanden
      if not os.path.exists(self.sessionpath):
         os.makedirs(self.sessionpath)
         

      self.cookie = Cookie.SmartCookie()
      self.loadCookie()
      self.newSession()

      # Attribute Laden wenn Cookie 'sid' gesetzt
      if self.cookie is not None:
         self.loadAttributes()

   # ### Sessionfilename
   #     Liefert Dateinamen des Sessionfiles
   #
   def getSessionFileName(self):
      'Liefert basierend auf dem Cookieeintrag den Dateinamen'
      return self.sessionpath+'/'+self.sid+'.ses'

   def lifetime(self):
      'Loescht alle Sessiondatein welche aelter als die gegebene Lebenszeit hat'
      filename = self.getSessionFileName()
      if os.path.exists(filename):
         ftime = os.stat(filename).st_mtime
         delta = int(time()-ftime)/60
         if delta > self.sessionlifetime:
            os.unlink(filename)
         else:
            pass
      else:
         if 'sid' in self.cookie:
            del self.cookie['sid']

   def loadAttributes(self):
      'Befuellt Buffer vom Attributfile'
      if os.path.exists(self.getSessionFileName()):
         filename = self.getSessionFileName()
         fSession = open(filename,'r')
         self.attributes = pickle.load(fSession)
         fSession.close()
      else:
         if 'sid' in self.cookie:
            del self.cookie['sid']

   def generateSessionId(self):
	    'Erzeugen einer Session ID '
	    retval = base64.b64encode(os.urandom(16)).replace('==','')
	    retval = retval.replace('/','_')
	    retval = retval.replace('+','_')
	    return retval

   def newSession(self):
      'Anlegen einer neuen Session'

      # wenn keine Cookies vorhanden sind
      if 'sid' not in self.cookie:
         self.sid = self.generateSessionId()
         fSession = open(self.getSessionFileName(),'w')
         pickle.dump(self.attributes,fSession)
         fSession.close()
         self.cookie['sid'] = self.sid
      else:
         self.lifetime()

   def remove(self):
      'Entfernen Session'
      try:
         os.unlink(self.getSessionFileName())
      except:
         return
      del self.cookie['sid']
      self.purge()

   def purge(self):
      'entfernen alter Sessiondateien'
      path = self.sessionpath
      
      for file in os.listdir(path):
         filename = path+'/'+file            
         ftime = os.stat(filename)[7]
         delta = int(time()-ftime)/60            
         if (delta > self.sessionlifetime):
            os.unlink(filename)

   def setCookie(self):
      'Schreibt Cookies in den Header'
      print self.cookie


   def loadCookie(self):
      'Laed den Inhalt des Cookie in die Variable self.sid'
      self.sHHTP_COOKIE = os.environ.get('HTTP_COOKIE','')
      if self.sHHTP_COOKIE is None:
         return None

      # Cookies wurden gefunden
      # Daten initalisieren
      self.cookie.load(self.sHHTP_COOKIE)
      self.sid = self.getSID()

   def getSID(self):
      'Liefert den Inhalt der Cookievariable sid'
      if 'sid' in self.cookie:
         return self.cookie['sid'].value
      else:
         return None

   def setAttribute(self,name=None,value=None):
      'Setzt den Inhalt des Parameters value in die Session'
      fSession = open(self.getSessionFileName(),'w')
      self.attributes[name] = value
      pickle.dump(self.attributes,fSession)
      fSession.close

   def removeAttribute(self,name=None):
      'loescht den Inhalt des Attributes'
      self.sid = self.cookie['sid'].value
      del self.attributes[name]
      fSession = open(self.getSessionFileName(),'w')
      pickle.dump(self.attributes,fSession)
      fSession.close

   def removeAllAttributes(self):
      'loescht den Inhalt aller Attributes'
      self.sid = self.cookie['sid'].value
      self.attributes = dict()
      fSession = open(self.getSessionFileName(),'w')
      pickle.dump(self.attributes,fSession)
      fSession.close

   def getAttribute(self,name=None):
      'Liefert den Inahlt eines Attributes oder None, wenn nicht vorhanden'

      if name==None:
         raise(Exception('Fehlender Attributname (Parameter name)'))

      if name not in self.attributes:
         return None

      return self.attributes[name]
