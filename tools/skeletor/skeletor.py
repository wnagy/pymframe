# -*- coding: iso-8859-15 -*-
"""
Grundmodul der Entwicklungsumgebung

"""
from optparse import OptionParser
import sys
import os
import re
import shutil

endSkeletor = False

options = None
args    = None


def readTemplateFile(tmpname):
   fpath = sys.argv[0]
   fpath = os.path.split(fpath)[0]
   f = open(fpath+'/{0}'.format(tmpname))
   b = f.read()
   f.close()
   return b

def makeFile(path,filename):
   path = path.rstrip('/')
   fPath = '{0}/{1}'.format(path,filename)
   f = open(fPath,'w')   
   f.close()

def doClone(options,args):

   SHEBANG5 = r"#!c:\Python25\python.exe"
   SHEBANG6 = r"#!c:\Python26\python.exe"
   SHEBANG7 = r"#!c:\Python27\python.exe"
   SHEBANGUX= r'#!/usr/bin/python'
   shebang = SHEBANG7


   cwd = os.path.split(os.getcwd())[0]
   appname = ''
   if len(args) < 1:
      appname = raw_input("Anwendungsname (leer = exit): ")
      appname = appname.strip(' ')
      if appname == '': return
   else:
      appname = args[1]


   current = os.getcwd()
   goal = os.path.split(os.getcwd())[0]+'/'+appname
   current = current.replace('\\','/')
   goal = goal.replace('\\','/')

   if os.path.exists(goal):
      if options.force:
         shutil.rmtree(goal)
      else:
         print ("Anwendung "+appname+" Bereits vorhanden. Verwenden -f um zu ueberschreiben.")
         return

   shutil.copytree(current, goal)

   if shebang != '':
      sF = open(goal+'/scripts/start.py','r')
      buffer = sF.readlines()
      sF.close()
      buffer[0] = shebang
      sF = open(goal+'/scripts/start.py','w')
      sF.write(''.join(buffer))
      sF.close()


   rFile = open('{0}/WEB-INF/mvc/root/view.tpl'.format(goal),'w')
   rFile.write ("""<!-- Viewer -->
   <%
   import time
   %>
   <h1>Willkommen bei  {0}</h1>
   Datum <%out(time.strftime('%d.%m.%Y'))%>
   <pre style="font-family:courier">
                  __  _______
       ___  __ __/  |/  / __/______ ___ _  ___
      / _ \/ // / /|_/ / _// __/ _ `/  ' \/ -_)
     / .__/\_, /_/  /_/_/ /_/  \_,_/_/_/_/\__/
    /_/   /___/

   </pre>""".format(appname))

   rFile.close()
   rFile = open('{0}/WEB-INF/templates/login.tpl'.format(goal),'r')
   buffer = rFile.read()
   rFile.close()
   welcome=r'    <h1 style="font-size:smaller;text-align:center;margin:auto;width:90%;">Willkommen bei pyMFrame</h1>'
   newWelcome = '    <h1 style="font-size:smaller;text-align:center;margin:auto;width:90%;">Willkommen bei {0}</h1>'.format(appname)
   buffer = buffer.replace(welcome,newWelcome)
   rFile = open('{0}/WEB-INF/templates/login.tpl'.format(goal),'w')
   rFile.write(buffer)
   rFile.close()

   rFile = open('{0}/WEB-INF/templates/default.tpl'.format(goal),'r')
   buffer = rFile.read()
   rFile.close()
   buffer = buffer.replace(welcome,newWelcome)
   rFile = open('{0}/WEB-INF/templates/default.tpl'.format(goal),'w')
   rFile.write(buffer)
   rFile.close()

   print """
   Die Datenbank befindet sich in ./WEB-INF/datastore/database/database.db3
   """

def doHelp(options,args):
   try:
      what = args[1]
   except:
      print 'Hilfe fuer was?'
      print 'help [quit|exit|create|clone]'

      return
   if what in ['create','make']:
      print 'Erzeugen [controller|domain]'
      try:
         what = args[2]
      except:
         print 'help make|create [controller|domain]'
         return
      if what=='controller':
         print "\nusage: make|creat controller --path=<pfad> --domain=<Domainname>"
         print "\nIst der Controler bereits vorhanden, wird die Funktion abgebrochen.\n"
         print "\nWird die option -f (force) notiert, wird keine Ueberpruefung vorgenommen ob der Controller bereits vorhanden ist."
         print "HINT: Das Programm kann keine Ueberpruefungen durchfuehren,\nob die Domain oder der Eintrag im Menue vorhanden ist!"
         print "Der Pfad muss im ./conf/menu.py selbstaendig eingetragen werden!\n"
      if what=='domain':
         print "\nusage: make|create domain <domainname> --key=<primarikey-name> --table=<domain-name>"
         print "\nIst die Domain bereits vorhanden, wird die Funktion abgebrochen.\n"
   elif what in  ['quit','exit']:
      print 'Beenden des Skeletors'
   elif what == 'clone':
      print 'clone erzeugt eine 100% Kopie der aktellen Anwendung.'+\
            'Ist an sich nur in der Anwendung pymframe brauchbar. Wenn man weiss was man tut auch bei anderen moeglich.'+\
            'clone <neuer-app-name>'+\
            'Wenn die Anwendung bereits vorhanden ist wird das Programm abgebrochen.'+\
            'Die option -f LOESCHT! die Anwendung und legt diese neue an.'

def createMenu(path,controller,text):
   cwd      = os.getcwd()
   mFileName = cwd+'/WEB-INF/conf/menu.py'

   mF = open(mFileName,'r')
   regEndEntry = re.compile('}\s*,\s*\]',re.M)

   src = mF.read()
   mF.close()

   if re.search(path,src):
      print " [warning] Menueeintrag {0} bereits vorhanden, nicht angelegt".format(path)
      return

   e = "},\n     {\n       'path':'%(path)s',\n       'controller':'%(controller)sController',\n       'text':'%(text)s',\n       'display':True,\n       'rights':None,\n     },\n    ]\n" % {
      'path':path,
      'controller':controller,
      'text':text
      }

   print " +Controller erzeugt"
   if re.search(regEndEntry,src):
      src = re.sub(regEndEntry,e,src)
      mF = open(mFileName,'w')
      mF.write(src)
      mF.close()
      print " +Controller in Menu eingetragen\n"
   else:
      print "** Kann in ./conf/menu.py' das Menuendekennzeuchen '},]' nicht finden.\n"
      print "   Menueintrag:\n   {0}".format(e)


def makeController(options,argv):

   if len(args) < 3:
      print 'Es fehlt der Controllername'
      return
   controllername = args[2]

   path = options.path
   if path == '': print 'Es fehlt die --path option'; return

   domain = options.domain
   if domain == None: print "--domain nicht angegeben";  return


   path = path.rstrip('/')

   cwd      = os.getcwd()
   goalDir = "./WEB-INF/mvc{0}".format(path)
   goalDir = goalDir.replace('\\','/')
   
   if not options.force:
      if os.path.exists(goalDir):
         print "*** Controller bereits vorhanden"
         return
   try:
      os.makedirs(goalDir)
      makeFile(goalDir,'__init__.py')
   except: pass

   controllername = os.path.split(goalDir)[1]
   controllername = controllername.title()

   f = open('{0}/{1}Controller.py'.format(goalDir,controllername),'w')


   buffer = readTemplateFile('controller.tpl')
   buffer = buffer.replace('{0}',controllername)
   buffer = buffer.replace('{1}',domain)
   buffer = buffer.replace('{2}',domain.lower())
   print>>f,buffer
   f.close()

   f = open('{0}/grid.tpl'.format(goalDir),'w')
   buffer = readTemplateFile('viewer.tpl')
   buffer = buffer.replace('{0}',domain.replace('Domain',''))

   print>>f,buffer
   f.close()
   createMenu(path,controllername,controllername)


def createDomain(options,args):

   sDomain = args[2]
   print sDomain
   sPrimarykey = options.primarykey
   if sPrimarykey == None:
      print "Kein Primary Key (--key) angegeben"
      return

   sTable = options.table
   if sTable == None :
      print "Kein Tabellenname (--table) angegeben"
      return

   filename = "./WEB-INF/mvc/domain/{0}.py".format(sDomain.lower())
   print "Erzeuge:{0}\n Tabelle: {1}\n PK: {2}\n in {3}".format(sDomain,sTable,sPrimarykey,filename)
   if os.path.exists(filename):
      if not options.force:
         print "Domain {0} existier bereits".format(sDomain)
         return
   tpl = readTemplateFile('domain.tpl')

   buffer = tpl % {'domain':sDomain, 'key':sPrimarykey, 'table':sTable}

   f = open(filename,'w')
   print >>f,buffer
   f.close()

def doMake(options,args):
   subcom = {
      'controller':makeController,
      'domain':createDomain,
      'menu':None
      }
   if not args[1] in subcom.keys():
      print "Ungueltiges Subkommandoe {} in make".format(args[1])
      return

   subcom[args[1]](options,args)

parser = OptionParser('python skeletor.py COMMAND [options...]')
parser.add_option('-p','--path',dest='path')
parser.add_option('-d','--domain',dest='domain')
parser.add_option('-k','--key',dest='primarykey')
parser.add_option('-t','--table',dest='table')
parser.add_option('-e','--exclude',dest='exclude')
parser.add_option('-f','--force',dest='force',action='store_true')


(options, args) = parser.parse_args()
commands = {
   'help'      :doHelp,
   'make'      :doMake,
   'create'    :doMake,
   'clone'     :doClone
   }

def checkCommand(options,args):
   if len(args) < 1: return

   if args[0] in commands:
      commands[args[0]](options,args)
   else:
      print "ungueltiges Kommando"

if len(args) < 1:
   # Interaktiver Modus
   print '''
                  __  _______
       ___  __ __/  |/  / __/______ ___ _  ___
      / _ \/ // / /|_/ / _// __/ _ `/  ' \/ -_)
     / .__/\_, /_/  /_/_/ /_/  \_,_/_/_/_/\__/
    /_/   /___/

   Einrichten einer pyMframe Anwendung

   W. Nagy

   quit|exit beendet den interaktiven Modus
   help bietet Hilfe

   '''
   while not endSkeletor:
      cli = raw_input('skeletor>')
      cli = cli.strip()
      if cli in ['quit','exit']:
         endSkeletor = True
         continue

      if cli == '': continue
      save0=sys.argv[0]
      sys.argv = [save0]+cli.split(' ')

      (options, args) = parser.parse_args()
      checkCommand(options,args)
else:
   checkCommand(options,args)

