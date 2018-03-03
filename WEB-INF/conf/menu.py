# -*- coding: iso-8859-15 -*-
import cgi
from menubase import MenuBase

class Menu(MenuBase):

   # default path
   path = '/'

   # ####
   # Menueeintraege:
   #
   # path:          definiert den Eintrag
   #
   # controller:    Gibt die Klasse an welche
   #                ausgefuehrt werden soll
   #
   # text:          Anzeigetext im Menue
   #                HINT: wird dieser Eintrag nicht
   #                      angegeben, so wird der Menuepunkt
   #                      nicht angezeigt.
   #
   # diplay:        [True | False]
   #                 Wir die Opton auf False gesetzt, so
   #                 wir der Menueeintrag nicht angezeigt.
   #                 Der Eintrag kann im Controller durch die
   #                 Methode self.setEntryDisplay(path='pfad', mode=[True | False])
   #                 umegesetzt werden.
   #                 Wird diese Option nicht angegeben wird True angenommen
   #
   entries=[
     {'path':'/root/','text':'@header:Funktionen','display':True},
     {  # Root Controller - dieser muss vorhanden sein.
        'path':'/root',
        'controller':'RootController',
        'text':'start'
     },
     {  # Authentifizierung Controller - dieser muss vorhanden sein.
        'path':'/authen',
        'controller':'AuthenController'
     },
     # ### DIENSTE ########################################
     {'path':'/root/dienste/','text':'@header:Dienstprogramme','display':True},
     {
       'path':'/root/dienste',
       'controller':'DiensteController',
       'text':'Dienste',
       'display':True,
       'rights':['admin'],
       'title':'Dienstfunktionen'
     },
     {'path':'/root/dienste/changepassword/','text':'@header:Passwort','display':True},
     {
       'path':'/root/dienste/changepassword',
       'controller':'ChangepasswordController',
       'text':'Passwort umsetzen',
       'display':True,
       'rights':None,
     },
     # ### E X T R A S ####################################################
     {'path':'/root/extras/','text':'@header:Extras','display':True},
     {
       'path':'/root/extras',
       'controller':'ExtrasController',
       'text':'Extras',
       'display':True,
       'rights':['admin'],
       'title':'Spezielle Funktionen',
     },         
     {'path':'/root/extras/lov/','text':'@header:Lov','display':True},
     {
       'path':'/root/extras/lov',
       'controller':'LovController',
       'text':'Lov',
       'display':True,
       'rights':['admin'],
       'title':'Systemdaten',
     },
     {'path':'/root/extras/user/','text':'@header:User','display':True},
     {
       'path':'/root/extras/user',
       'controller':'UserController',
       'text':'User',
       'display':True,
       'rights':['admin'],
       'title':'Verwalten von Benutzer',
     },
     {'path':'/root/extras/maintenance/','text':'@header:Maintenace','display':True},
     {
       'path':'/root/extras/maintenance',
       'controller':'MaintenanceController',
       'text':'Maintenance',
       'display':True,
       'rights':['admin'],
     },
     ]

