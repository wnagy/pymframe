import sys
import os

sys.path.extend(['..','../..','../../../WEB-INF/mvc','../../../WEB-INF/site-packages'])

from dbaccess.core         import *
from domain.testdomain     import TestDomain
from dateconverter         import Dateconverter

db = Database('oracle','SCOTT','TIGER','v9i','194.37.51.27','1521')

def hasException (code):
   """Prueft ob bei uebergebenen Code eine Exception auftritt"""

   retval = False
   try:
      eval(code)
   except:
      return True
   return False

dc = Dateconverter()

t1 = TestDomain(db)
t2 = TestDomain(db)

t1.deleteAll(where='1=1')
t1.clear()
t1.tstID = 1
t1.tstDate = dc.fromString('1.1.2010')

t2.tstID=23
t2.tstDate = t1.tstDate

print t1.tstDate
print t2.tstDate

print type(t1.tstDate)
print type(t2.tstDate)

t1.insert()
t2.insert()

print 'done'
