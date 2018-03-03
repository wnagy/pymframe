import os
import sys
import tempfile

class Sender(object):
   """
   Senden einer Datei
   """

   theFile           = None      # Filehandle
   name              = None      # Dateiname

   def __init__(self):
      # Spezielle Behandlung, wenn Binaere Daten unter Windows
      #
      if sys.platform == "win32":
         import msvcrt
         msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

   def send (self,fNamepath, fName):
      """
      Baut einen HTTP haeder zusammen und sendet 
      die Daten.
      """
      print "Content-Type: application/octet-stream"
      print 'Content-Disposition: attachment;filename="{0}" '.format(fName)
      print "Content-Length: {0}".format(fLength)
      f = open(fNamepath,'r')
      print f.read(),
      f.close()
      return False

   
   @staticmethod
   def getStaticTempFileName():
      xFile = tempfile.NamedTemporaryFile(delete=False,prefix='export-')
      xFileName = xFile.name
      xFile.close()
      return xFileName

   @staticmethod
   def send(oFile,fName):
      if sys.platform == "win32":
         import msvcrt
         msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

      fLength = os.path.getsize(oFile.name)      
      print "Content-Type: application/octet-stream"
      print 'Content-Disposition: attachment;filename="{0}" '.format(fName)
      print "Content-Length: {0}".format(fLength)
      print oFile.read(),
      return False

   def sendfile (self,tmpFileName, fName,delete=False):
      
      fLength = os.path.getsize(tmpFileName)
      print "Content-Type: application/octet-stream"
      print 'Content-Disposition: attachment;filename="{0}" '.format(fName)
      print "Content-Length: {0}".format(fLength)
      print
      f = open(tmpFileName,'rb')
      print f.read()
      f.close()
      if delete:  
         try:
            os.unlink(tmpFileName)
         except Exception,e:
            raise Exception(e)
            
      return False


if __name__=='__main__':
   sender = Sender()
   sender.send(r'c:\temp\x.py','test.py')
