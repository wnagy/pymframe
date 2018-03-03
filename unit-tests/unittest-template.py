import sys,os,re
import urllib
import logging


sys.path.extend([
   '../WEB-INF/mframe',       # Framework
   '../WEB-INF/mvc',          # Root fuer Domains
   '../WEB-INF',              # WEB-INF (Ressourcen)
   '../WEB-INF/addons',       # Zusatzmodule
   '../WEB-INF/site-packages' # Externe Zusatzmodule
   ])

from dbaccess.core            import *
from conf.config              import Config

reload(sys)
sys.setdefaultencoding("UTF-8")

import unittest
from StringIO import StringIO

from conf.config                 import Config
from domain.lovdomain            import LovDomain
from main                        import Mframe
from helper.utility              import Utility

class TestController(unittest.TestCase):

   def setLogger(self,mfw):
      mfw.logger = logging.getLogger("")
      mfw.logger.setLevel('INFO')
      fh = logging.FileHandler(mfw.config.logfile)
      formatter = logging.Formatter("%(asctime)s - %(message)s")
      fh.setFormatter(formatter)
      mfw.logger.addHandler(fh)

   
   def getMfw(self,query_string):
      os.environ['QUERY_STRING'] = query_string
      mfw = Mframe()
      mfw.db.user='admin'
      mfw.useAuthen = False
      mfw.config.useauthen = False
      mfw.init()
      self.setLogger(mfw)
      mfw.logger.info('RUN IN UNITTEST')
      return mfw
   
   def setUp(self):
      self.config = Config()

      self.db = Database('sqlite',self.config.sqlitefilename)
      self.db.user = 'roboter'


   def test_01(self):
      """
      Wir versuchen Root Aufzurufen
      """
      path = '/root'
      mfw = self.getMfw('path='+path)
      pat = '<title>pyMframe \[/root\]</title>'
      content = mfw.run()
      self.assertTrue(re.search(pat,content))

      # --- LOGIN ------------------------------
      params = {
         'path'                     : '/authen',
         'user'                     : 'admin',
         'password'                 : 'admin'
         }

      query_string = urllib.urlencode(params)

      save_stdout = sys.stdout
      capture = StringIO()
      sys.stdout = capture
      
      content = mfw.run()
      mfw.session.remove()

      sys.stdout = save_stdout

      # --- EINFUEGEN IN DB---------------------
      params = {
         'path'      : '/root/extras/lov',
         'action'    : 'save',
         'lovClass'  : 'CLASS',
         'lovKey'    : 'TEST',
         'lovValue'  : '++test++'
         }

      query_string = urllib.urlencode(params)
      cursor = self.db.cursorFactory()
      cursor.execute("PRAGMA read_uncommitted = ture;")
      self.db.begin()
      mfw = self.getMfw(query_string)
      pat = '<title>pyMframe \[/root\]</title>'
      content = mfw.run()
      self.assertFalse(re.search('id="flash"',content))
      self.db.rollback()


   def tearDown(self):
      """
      ENTFERNT alle Sessiondateien

      """
      mfw = self.getMfw('path=/root')
      mfw.session.sessionlifetime=-1
      mfw.session.purge()
      pass

if __name__ == '__main__':
   suite = unittest.TestLoader().loadTestsFromTestCase(TestController)
   unittest.TextTestRunner(verbosity=2).run(suite)