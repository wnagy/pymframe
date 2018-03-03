# -*- coding: iso-8859-15 -*-
import re,sys

class AuthenBase(object):
   """
   Basisklasse fuer Authentifizierung

    Die Autentifizierung basiert auf einer
    Sessionvariable namens user. Ist diese
    gesetzt gilt der Benutzer als angemeldet
   """

   user = None
   session = None
   usrrights = None
   userlist = {}
   db = None

   def __init__(self,session=None,db=None):
      """
      Konstruktor
      @param   session        Sessionobjekt
      """
      if db is not None: self.db = db
         
      if session is None:
         raise(Exception('Das Objekt muss mit einem Sessionobjekt befuellt werden'))
      self.session = session
      self.init()

   def getUser(self):
      """Liefert den aktuellen User"""
      return self.user

   def init(self):
      """ Initialisierung"""
      self.user      = self.session.getAttribute('user')      
      theUser = self.getUserinfo(user=self.user)
      self.usrrights    = theUser.get('rights')


   def isAuthenticated(self):
      """Liefert wahr, wenn benutzer vorhanden ist"""
      if self.user is not None:
         return True
      else:
         return False

   def getRights(self):
      """ABSTRAKT: 
      liefert eine Liste von Rechten, wenn Benutzer eingelogt
      """
      if self.isAuthenticated():
         return self.usrrights
      else:
         return []

   def hasRight(self,right=None):
      """
      Liefert True, wenn uebergebenens Recht in der Rechteliste vorhanden ist
      @param   right    Recht
      
      @return  [True|False] 
      """
         
      if self.isAuthenticated():            
         found = False
         # Gibt es keine Rechte
         # wird auf jeden Fall Wahr zurueckgeliefert
         if self.usrrights is None: return False
         right = right.split(':')[0]

         for theRight in self.usrrights:
            if right == theRight: found = True

         return found
      else:
         return False

   def checkRights(self,rights):
      """
      Prueft ob der Benutzer eines der uebergebene Rechte besitzt

      HINT:
         Es sind "negative" Rechte moeglich.
         ist in rights ein Recht mit einem vorlaufenden Minuszeit 
         behaftet z.B.: "-admin"  so wird falsch zurueckgeliefert,
         wenn das recht fuer den aktuellen Benutzer gefunden wird.

         Beispiel
            rights: develop,-admin
            userRights: "admin,user"
            Falsch da -admin in userRights vorhanden ist.
      """
      # Flag

      
      found = False

      # wurden Rechte gesetzt
      if rights is not None or rights==[]:
         if isinstance(rights,str): rights = rights.split(',')
            
         for right in rights:
            if right.startswith('-'):
               right = right[1:]
               if self.hasRight(right=right): return False
            else:
               if self.hasRight(right=right):
                  found = True         
      else:
         # Wenn keine Rechte im Menueintrag
         # auf jeden Fall anzeigen
         found = True
      
      return found

   def isReadonly(self,controllerrights):
      """
      Prueft ob der Benutzer zur Bereichtigung 
      des Controllers den readonly Qualifizerer (:r) gesetzt hat.

      HINT:
         Auf jeden Fall nicht readOnly wenn:
            + noch nicht angemeldet
            + die Controler Richteliste leer

      @param   controllerrights        Liste der rechte fuer diesen Controller

      @return  T/F
      """
      
      if (controllerrights or []) == []: return False
      if self.isAuthenticated():
         retval = False
         hasRO = False
         for theRight in controllerrights:
            auxTheRight = theRight.strip()
            
            for uright in self.getRights():
               theRight = auxTheRight.split(':')[0]
               if theRight == uright and auxTheRight.endswith(':r'):  return True
         return retval
      else:
         # Wenn noch nicht angemeldet immer Falsch
         return False


   def getUserinfo(self,user=''):
      """
      Liefert die Userinformatioenn oder eine leeres Dictionary,wenn nicht gefunden.
      @param   user  Benutzername
      """
   
      found = None
      for usr in self.userlist:
         if usr['user'] == user:
            found = usr

      if found is None:
         return {}
      else:
         return found


   def getPassword(self):
      """Liefert Passwort des aktuellen Benutzers oder None wenn nicht gefunden"""
      user = self.getUserinfo()
      if user != {}:
         return None
      else:
         return user['password']

   def authen(self):
      """Setzt die Rechte des Users, wenn eingeloggt"""
      if self.user is not None:
         user = getUserinfo()
         self.usrrights = user['rights']
