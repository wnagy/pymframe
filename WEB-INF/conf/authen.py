# -*- coding: iso-8859-15 -*-

# Authentifizierung
#

from authenbase            import AuthenBase
from domain.userdomain     import UserDomain

class Authen(AuthenBase):
   
   def cleanPassword(self,password):
      """
      Entfernt aus password den Praefix "md5:{" und abschliesende "}"
                                   oder "pbkdf2:{" und abschliessende "}"
      
      @param      password       Passwort

      @return     bearbeitetes Passwort
      """
      if password is None: password = ''
      if password.startswith('md5:{'):
         if not password.startswith('md5:{') and password.endswith('}'):
            raise Exception("Ungueltiger Passwortstring: {0})".format(password))         
         password = password[5:]
         password = password[:-1]

      if password.startswith('pbkdf2:{'):
         if not password.startswith('pbkdf2:{') and password.endswith('}'):
            raise Exception("Ungueltiger Passwortstring: {0})".format(password))
         password = password[8:]
         password = password[:-1]
      
      return password
      
   def getUserinfo(self,user=None):
      if user is None: return {}
      us = UserDomain(self.db)
      where = "usrUser = '{0}'".format(user)
      where = where.replace(';','')
      
      us.get(where=where)
            
      rights = None
      if us.usrRights is not None:
         rights = us.usrRights.split(',')
      
      return {
         'user':us.usrUser,
         'password':self.cleanPassword(us.usrPassword),
         'rights':rights
         }
      