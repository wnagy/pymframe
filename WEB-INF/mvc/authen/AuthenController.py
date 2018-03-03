# -*- coding: iso-8859-15 -*-
from controller import Controller
from dbaccess.core import *
from conf.config import Config

import hashlib
import binascii

from pbkdf2 import crypt

from conf.authen import Authen

class AuthenController(Controller):


   def __init__(self):
       pass

   def checkInternalUser(self,username,password):
      """
      Prueft ob interner User einlogen kann
      @param username                  username aus CGI
      @param password                  Passwrot aus CGI

      @return                          True/False

      HINT:
           setzt wenn OK Sessionattribute user

      """
      config = self.main.config
      
      userinfo = self.main.authen.getUserinfo(user=username)

      if config.authenMethod == 'md5':            
         hashPassword =  hashlib.md5(password).hexdigest()

         
      elif config.authenMethod == 'pbkdf2':
         auxPassword = crypt(password,config.authenSalt,10000)
         #raise Exception('pbkdf2:{'+auxPassword+'}')
         hashPassword = auxPassword
         
      else:
         raise ValueError('Methode bei Passwortverschluesselung fehlt (erlaubt md5,pbkdf2)')


      if  userinfo.get('user') == username and userinfo.get('password') == hashPassword :
         self.main.setAttribute('user',username)
         self.main.setAttribute('rights',userinfo.get('rights'))
         return True
      else:
         return False



   def login(self):

      username = self.main.cgiparam(name='user',nvl='')
      password = self.main.cgiparam(name='password',nvl='')
      print 'content-type: text/html\n\n'
      if self.checkInternalUser(username,password):
         # gibt Redirect aus
         print '''
            <html>
             <head>
              <meta http-equiv="refresh" content="0;url=./start.py?path=/root">
             </head>
            </html>
           '''
      else:
         print '''
            <html>
             <head>
              <meta http-equiv="refresh" content="0;url=./start.py?path=/root&flash=Fehlerhafter Benutzername oder Passwort!">
             </head>
            </html>
           '''

   def logout(self):
      self.main.session.remove()
      print 'content-type: text/html\n\n'
      print '''
         <html>
          <head>
           <meta http-equiv="refresh" content="0;url=./start.py?path=/root&flash=Abgemeldet!">
          </head>
         </html>
        '''


   def get(self):
      if self.main.cgiparam('action','') == 'logout':
         self.logout()
      else:
         self.login()
      return False

