# -*- coding: iso-8859-15 -*-

import re
from controller         import Controller
from viewhandler        import Viewhandler
from helper.utility     import Utility

from domain.userdomain import UserDomain


class ChangepasswordController(Controller):

   strength = ['Unsicher','Sehr schwach','Schwach','Mittel','Stark','Sehr stark']

   def checkPassword(self,password):
       score = 1
    
       if len(password) < 1:
           return 0
       if len(password) < 4:
           return 1
    
       if len(password) >=8:
           score = score + 1
       if len(password) >=10:
           score = score + 1
        
       if re.search('\d+',password):
           score = score + 1
       if re.search('[a-z]',password) and re.search('[A-Z]',password):
           score = score + 1
       if re.search('.[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]',password):
           score = score + 1
    
       return score
   
   def get(self):

      user = UserDomain(self.db)

      username = self.controller.session.getAttribute(name='user')

      if self.cgiparam('action') !=  'run':  
         self.view('changepassword.tpl',
            {
            'user':username
            }
            )
         return

      oldpw =self.cgiparam('oldpw')
      if oldpw == '': 
         self.flash("Altes Passwort fehlt")
         return True


      newpw =self.cgiparam('newpw')
      if newpw == '': 
         self.flash("Neus Passwort fehlt")
         return True

      checkpw =self.cgiparam('checkpw')
      if checkpw == '': 
         self.flash("Kontrolle fehlt")
         return True
 
      if newpw != checkpw:
         self.flash("Neues Passwort und Kontrolle stimmen nicht &uuml;berein")
         return True

      pwscore = self.checkPassword(newpw)

      if pwscore <= 3:
         self.flash('Passwort nicht sicher genug')
         return True

      user.getOverUsername(username)
      oldpw = user.toPassword(oldpw)      
      
      if user.usrPassword != oldpw:
         self.flash('Altes Passwort ungueltig')
         return True

      user.usrPassword = user.toPassword(newpw)
      user.update()
      self.render('Passwort ge&auml;ndert')


