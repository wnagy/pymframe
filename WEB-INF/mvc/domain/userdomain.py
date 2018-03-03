# -*- coding: iso-8859-15 -*-
from dbaccess.core   import *
import hashlib
import binascii
from conf.config import Config

from pbkdf2 import crypt

class UserDomain(Domain):
   usrID = None

   meta = {
      'tablename':'user',
      'primarykey':'usrID',
      'fields':{
         'usrID'              : {'dbfield':'usrID',            'type':'Integer'},
         'usrUser'            : {'dbfield':'usrUser',          'type':'String'},
         'usrPassword'        : {'dbfield':'usrPassword',      'type':'String'},
         'usrRights'          : {'dbfield':'usrRights',        'type':'String'},
         'usrRemarks'         : {'dbfield':'usrRemarks',       'type':'String'},
      }
   }

   def getDatasource(self,addempty=''):
      """
      Erzeugt eine Datasource fuer die Verwendung in
      taglib.promptinput
      """
      retval = []
      if addempty != None:
         retval.append(['',addempty])

      for domain in self.eachDomain(where=None,orderby=None):
         retval.append([domain.usrUser,"{0}".format(domain.usrUser)])
      return retval

   def toPassword(self,password,config=None):
      """
      Erzeugt eine MD5/pbkdf2 Passwortstring

      @param   password          Passwort in Klarschrift

      @return  Passwort mit format "[md5 | pbkdf2]:{[MD5-String]}"
      
      pbkdf2:{$p5k2$2710$3a7100f48b9e4156b369d265175a1fe1$oYklOUjvZP.CVMriOpocaW2Z514iJ77/}
      """
      if config is None:
         config = Config

      if config.authenMethod == 'md5':            
         hashPassword =  'md5:{{{0}}}'.format(hashlib.md5(password).hexdigest())
      elif config.authenMethod == 'pbkdf2':
         auxPassword = crypt(password,config.authenSalt,10000)
         hashPassword =  'pbkdf2:{{{0}}}'.format(auxPassword)
      else:
         hasPassword = password

      return hashPassword

   def onInsert(self):
      if self.usrPassword is None: return True
      hashPassword =  self.toPassword(self.usrPassword)
      self.usrPassword = hashPassword
      return True

   def onUpdate(self):
      if self.usrPassword is None: return True
      if self.usrPassword.startswith('pbkdf2:{') or self.usrPassword.startswith('md5:{'):
         hashPassword =  self.toPassword(self.usrPassword)      
         self.usrPassword = hashPassword
      return True

   def getOverUsername(self,username):
      self.get(where='usrUser = "{0}"'.format(username))
      return self.isOk
   