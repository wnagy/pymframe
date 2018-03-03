"""
Hilfsklasse zum Internationlisierung.

usage

_ = Translate('en.lang','en').translateit
print _('eins')


Beispiel der Uebersetzungsdatei

[en]
eins=one
zwei=two
Fenster=window
help:dies
 ist ein Absatz
 ende des Absatzes.
help:
 <h2>Ausf&uuml;llhinweise</h2>
 <p>
 Bitte f&uuml;lle untenstehendes Formular sorgf&auml;ltig aus.<br />
 <strong>Mit * (Stern) gekennzeichnet Felder sind Pflicht!</strong>
 ...
"""
import ConfigParser
import re

class Translate:
    trans = ConfigParser.ConfigParser()

    curLang = None

    def __init__(self,lfile,language):
       self.trans.optionxform = str
       self.trans.read(lfile)
       self.curLang = language
       pass

    def translateit(self,phrase=None,language=None):
       lang = language or self.curLang

       try:
          sText = self.trans.get(lang,phrase)
          sText = re.sub(r'\n\s*\.\s*\n','\n \n',sText)
          return sText
       except:
          return phrase

if __name__ == '__main__':
   _ = Translate('en.lang','en').translateit
   print _('eins')
   print _('xxeins')
   #print _('Fenster')
   #print _('help')