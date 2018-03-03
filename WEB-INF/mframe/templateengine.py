# -*- coding: iso-8859-15 -*-
from conf.config import Config
from string import Template

class TemplateEngine:
   template=''
   tplFileName = ''
   config = None

   def __init__(self,config=None):

      self.config = config or Config()
      self.tplFileName = config.defaulttemplate
      self.readTemplateFile()
      
   def readTemplateFile(self):
      fIn = open(self.config.templatepath+'/'+self.tplFileName,'r')
      buffer = fIn.read()
      fIn.close()
      self.template = Template(buffer)
   

   def get(self,map):
      return self.template.substitute(map)
      pass