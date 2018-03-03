@echo off
rem = """
@rem Startet den WEB-SERVER
@rem 
@rem 
set zip="%cd%\..\..\bin\7zip\7z"
rd /S /Q .\distribution\
set pythonhome=
set python="..\..\bin\python27\app\python.exe"
if not exist %python% (
   echo.
   echo Kann keine Pythoninterpreter finden
   echo Programmabbruch
   echo.
   goto endofPython
   )
title Build
rem Start das aktuelle Script mit Python
"%python%" -x "%~f0" %1 %2 %3 %4 %5 %6 %7 %8 %9
goto endofPython """
"""
Bildet die Anwendung zum Demploy
"""
import os
import shutil
import subprocess
import re


cwd = os.getcwd()

# ###
# 
appname = 'pymframe'
#
# enalble this on produktion
# appname = os.path.split(cwd)[1]

adddir = ''

dstdir = os.path.abspath(cwd+'/distribution/'+appname).replace('\\','/')+'/'
srcdir = cwd.replace('\\','/')+'/'

# ## Anlegen des Distributionsverzeichnisses
try:
   shutil.rmtree(dstdir)
except: pass

os.makedirs(dstdir+adddir)

dstdir += adddir

shutil.copyfile(srcdir+'index.html',dstdir+'index.html')
shutil.copyfile(srcdir+'.htaccess',dstdir+'.htaccess')
shutil.copyfile(srcdir+'setup.sh',dstdir+'setup.sh')
shutil.copyfile(srcdir+'favicon.ico',dstdir+'favicon.ico')

dirs = ['css',
        'images',
        'info']

for dir in dirs:
   shutil.copytree(srcdir+dir,dstdir+'/'+dir)

os.mkdir(dstdir+'/scripts')

#shutil.copyfile(srcdir+'/scripts/start.py',dstdir+'/scripts/start.py')
shutil.copytree(src=srcdir+'/WEB-INF',dst=dstdir+'WEB-INF',ignore=shutil.ignore_patterns('*.pyc','*.ses'))
shutil.rmtree(dstdir+'WEB-INF/datastore')

f = open(srcdir+'/scripts/start.py')
lines = f.readlines()
f.close()

for ln in range(len(lines)):
   line = lines[ln]

   m = re.search("\.version\s*=\s*'(.*)'",line)
   if m:
      lfdnr = m.group(1)[-3:] 
      verno = m.group(1)[:-3]
      sz = len(lfdnr)
      n = int(lfdnr)
      n += 1
      fmt = '{0:0%dd}' % sz
      lfdnr = fmt.format(n)
      v = '{0}{1}'.format(verno,lfdnr)
      lines[ln] = "mfw.version = '{0}'\n".format(v)
      print lines[ln]

print 'shebang: '+lines[0].strip(), ' --> ',
lines[0] = '#!/usr/bin/python\n'
print lines[0]

f = open(srcdir+'/scripts/start.py','wb')
print>>f,''.join(lines)
f.close()

shutil.copyfile(srcdir+'/scripts/start.py',dstdir+'/scripts/start.py')

rem = """
:endofPython 
pushd .\distribution

if exist pymframe.zip (
   del pymframe.zip
   )

%zip%  a  -r -tzip -x!pymframe.zip pymframe
popd
pause
"""
