@echo off
rem = """
@rem Startet den WEB-SERVER

set python="..\..\bin\python27\App\python.exe"

if not exist %python% (
   echo.
   echo Kann keine Pythoninterpreter in %python% finden
   echo Programmabbruch
   echo.
   pause
   goto endofPython
   )

title SCHLIESSEN DIESES FENSTERS BEENDET DIE ANWENDUNG!
rem Start das aktuelle Script mit Python
"%python%" -x "%~f0" %1 %2 %3 %4 %5 %6 %7 %8 %9
goto endofPython """

# Your python code goes here ..

import CGIHTTPServer
import BaseHTTPServer
import os
import sys

import subprocess

# ### CONFIG-SECTION
#
PORT = 8000

# if None no broser startup
BROWSER=[r"..\..\bin\IronPortable\Iron\iron.exe","--incognito","--start-maximized","--no-default-browser-check","--disable-translate","--disable-sync","--disable-panels","http://localhost:8000"]
#BROWSER=None
class Handler(CGIHTTPServer.CGIHTTPRequestHandler):


   cgi_directories = ["/scripts"]

   def _url_collapse_path_split(self,path):
       # Similar to os.path.split(os.path.normpath(path)) but specific to URL
       # path semantics rather than local operating system semantics.
       rest = ''
       # Filter cgi parameter
       if path.find('?') != -1:
          (path,rest) = path.split('?')

       if rest != '': rest = '?'+rest
          
       self.log_message('rest: %s',rest)

       path_parts = []
       for part in path.split('/'):
           if part == '.':
               path_parts.append('')
           else:
               path_parts.append(part)

       # Filter out blank non trailing parts before consuming the '..'.
       path_parts = [part for part in path_parts[:-1] if part] + path_parts[-1:]
       if path_parts:
           tail_part = path_parts.pop()
       else:
           tail_part = ''
       head_parts = []
       for part in path_parts:
           if part == '..':
               head_parts.pop()
           else:
               head_parts.append(part)
       if tail_part and tail_part == '..':
           head_parts.pop()
           tail_part = ''

       return ('/' + '/'.join(head_parts), tail_part+rest)

   def is_cgi(self):
      splitpath = self._url_collapse_path_split(self.path)
      if splitpath[0] in self.cgi_directories:
         self.cgi_info = splitpath
         return True
      return False

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

print ' '
print "serving at port:", PORT
print '**********************************************'
print '* NICHT BEENDEN SOLANGE DIE ANWENDUN LAEUFT! *'
print '**********************************************'
print ' '
print 'Aufrufen im Browser durch: http://localhost:8000'
print ' '
print 'Beenden durch Strg+Pause'
print ' '

# STARTEN Browser
if BROWSER != None: 
   checkbrowser=BROWSER[0]
   if not os.path.exists(checkbrowser):
      print "Kann Browser {0} nicht finden".format(checkbrowser)
      raw_input("Programmauruf im Browser ihres Vertrauens durch\nhttp://localhost:"+str(PORT)+'\n\n')
   else:
      subprocess.Popen(BROWSER)

httpd.serve_forever()
rem = """
:endofPython """
