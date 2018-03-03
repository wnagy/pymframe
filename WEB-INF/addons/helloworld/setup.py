# -*- coding: utf-8 -*-
"""
Helloworld Addon
W. Nagy

Minimales Plugin

Verwendet lokales Config und Controller des aufrufenden Programms.

"""
from helloworld.conf.config           import Config as HelloworldConfig

class Helloworld(object):

   controller = None

   def __init__(self,controller):
      self.controller = controller

   def get(self):
      config = HelloworldConfig()
      self.controller.render('The Helloworld says: "{0}"'.format(config.greetings))
