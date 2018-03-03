# -*- coding: iso-8859-15 -*-

from template import PSP
import cgi
import traceback

import os

class Controller:
   """
   Basisklasse fuer eine Controller
   Die Klasse wird vom Framework automatisch
   generiert und initialisiert.

   """
   html                 = ''
   addEntry             = None
   setEntryDisplay      = None
   setEntryParam        = None
   path                 = ''
   db                   = None
   main                 = None
   cgiparam             = None
   form                 = None
   config               = None


   def render(self,text=''):
      """
      Einfuegen String in Buffer.

      Beispiel: self.render("Hallo Welt")

      @param   text        Auszugebender Text

      """
      self.html = self.html + text


   def view(self,filename,param=None,importcgi=False):
      """
      Aufrufen Viewer
      
      @param   filename          Filenamen des Viewer
      @param   param             Binding Variable fuer den 
                                 Viewer, welch dort verwenden werden koennen.
      @param   importcgi         Felder eine Form werden automatisch
                                 aus dem CGI befuellt

      @return     True|False     Je nach erfolgt
      """
      if filename.startswith('mvc://'):
         viewerfile = self.config.mvcpath+'/'+filename[6:]         

      elif filename.startswith('file://'):
         viewerfile = filename[7:]

      else:
         viewerfile = self.config.mvcpath+self.path+'/'+filename

      viewerfile = os.path.normpath(viewerfile.replace('\\','/'))      
      
      try:
         fViewer = open(viewerfile,'r')
      except Exception,e:
         self.html= self.main.appException(self.controllerfilename,str("Kann VIEWER nicht finden:<br />%(filename)s<br />%(error)s" % {'filename':filename,'error':e}))
         return False

      text = fViewer.read()

      try:
         psp = PSP(template=text,filename=filename,cgiparam=self.cgiparam,isReadonly=self.isReadonly,controller=self)
      except Exception,e:
         self.html= self.main.appException(self.controllerfilename,str("Fehler im Template:<br />%(filename)s<br />%(error)s" % {'filename':filename,'error':e}))
         return False

      # Importiert alle CGI Parameter in Param
      if importcgi:
         self.form=cgi.FieldStorage()
         for fld in self.form:
            param[fld]=self.form[fld].value
      value = ''
      
      value = psp.render(param)

      self.html = self.html + value
      return True

