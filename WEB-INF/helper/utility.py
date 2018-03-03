# -*- coding: iso-8859-15 -*-

"""
Verschiedene Hilfs- und Wartungsmethoden
"""
import random
import string

class Utility(object):

   @staticmethod
   def normalizeFilter(_filter):
      """
      Bearbeiten des Filters
      ''          -->   %
      None        -->   %
      *           -->   %
      ?           -->   _
      """
      _filter = '' if _filter == None else _filter

      _filter = _filter.rstrip(' ')
      _filter = '%' if _filter == '' else _filter
      _filter = _filter.replace('*','%')
      _filter = _filter.replace('?','_')

      return _filter

   @staticmethod
   def getpassword(minlen=8,maxlen=8):
      """
      Generiert ein Passwort
      @param   minlen         minimale Länge
      @param   maxlen         maximale Länge
      """

      pwdlen=random.randint(minlen,maxlen)
      zeichensatz=string.lowercase+string.uppercase+string.digits
      passwort=""

      for zeichen in range(pwdlen):
          zufallszeichen=random.randint(0, 61)
          passwort+=zeichensatz[zufallszeichen]

      return passwort
