import sys
import time

sys.path.extend(['..'])


from dateconverter import Dateconverter

def hasException (code):
   """Prueft ob bei uebergebenen Code eine Exception auftritt"""

   retval = False
   try:
      eval(code)
   except:
      return True
   return False

dc = Dateconverter()
assert(hasException("dc.giveAsANSIDate()"))

assert(dc.fromString('1.1.2011') == '2011-01-01T00:00')
assert(dc.fromString('01.01.2011') == '2011-01-01T00:00')
assert(dc.fromString('2011-01-01')== '2011-01-01T00:00')
assert(dc.fromString('2011-01-01')== '2011-01-01T00:00')

assert(dc.fromString('2011-01-01T01:01')== '2011-01-01T01:01')
assert(dc.fromString('2011-01-01T01:01:33')== '2011-01-01T01:01:33')


assert(dc.fromString('31.12.2011 11:22:33')== '2011-12-31T11:22:33')
assert(dc.fromString('31.12.2011 10:20')== '2011-12-31T10:20')

assert(hasException("dc.fromString('31.2.2011')"))
assert(hasException("dc.fromString('31.2.2011 24:01')"))
assert(hasException("dc.fromString('31.2.2011 23:59:61')"))
assert(hasException("dc.fromString('31.2.2011 99:00')"))
assert(hasException("dc.fromString('2011-01-01T01:01:99')"))
assert(hasException("dc.fromString('2011-01-01T25:01:00')"))
assert(hasException("dc.fromString('2011-01-01T24:01:00')"))
assert(hasException("dc.fromString('2011-01-01T23:61:00')"))


dc.fromString('31.12.2011 11:22:33')
assert(dc.giveAsANSIDate() == '2011-12-31')
dc.fromString('31.12.2011 11:22')
assert(dc.giveAsANSIDate() == '2011-12-31')
assert(dc.giveAsANSIDateTime() == '2011-12-31T11:22')

dc.fromString('31.12.2011 11:22:33')
assert(dc.giveAsANSIDateTime(secs=True) == '2011-12-31T11:22:33')

dc.fromString('31.12.2011')
assert(dc.giveAsANSIDateTime(secs=True) == '2011-12-31T00:00:00')

dc.clear()
# pruefen ob Exception geworfen wird wenn Datum nicht initialisiert
assert(hasException("dc.giveAsANSIDate()"))

# Give mit Datum
assert(dc.giveAsANSIDate('31.12.2011') == '2011-12-31')
assert(dc.giveAsANSIDate('2011-12-31') == '2011-12-31')
assert(dc.giveAsANSIDate('31.12.2011 11:22') == '2011-12-31')
assert(dc.giveAsANSIDateTime('31.12.2011 11:22') == '2011-12-31T11:22')
assert(dc.giveAsANSIDateTime('31.12.2011 11:22:33',secs=True) == '2011-12-31T11:22:33')
assert(dc.giveAsANSIDateTime('31.12.2011 11:22:33',True) == '2011-12-31T11:22:33')
assert(dc.giveAsANSIDateTime(secs=True,value='31.12.2011 11:22') == '2011-12-31T11:22:00')


# Datumsfehler
assert(hasException("dc.giveAsANSIDate('31.2.2011')"))

dc.clear()
assert(dc.giveAsGermanDate('2011-01-01') == '01.01.2011')
assert(dc.giveAsGermanDate('2011-01-01','%d. %b %Y') == '01. Jan 2011')
assert(dc.giveAsGermanDate(format='%d. %b %Y',value='2011-01-01') == '01. Jan 2011')

assert(dc.giveAsGermanDateTime('1.1.2011 11:22') == '01.01.2011 11:22')
assert(dc.giveAsGermanDateTime('1.1.2011 11:22:33',secs=True) == '01.01.2011 11:22:33')
assert(dc.giveAsGermanDateTime('1.1.2011 11:22',secs=True) == '01.01.2011 11:22:00')
assert(dc.giveAsGermanDateTime('1.1.2011',secs=True) == '01.01.2011 00:00:00')

assert(dc.giveAsGermanDate(value=None,nvl='now') == time.strftime('%d.%m.%Y',time.localtime()))
assert(dc.giveAsGermanDateTime(value=None,nvl='now') == time.strftime('%d.%m.%Y %H:%M',time.localtime()))

assert(dc.giveAsGermanDate(value=None,nvl='jetzt') == time.strftime('%d.%m.%Y',time.localtime()))
assert(dc.giveAsGermanDateTime(value=None,nvl='jetzt') == time.strftime('%d.%m.%Y %H:%M',time.localtime()))

assert(dc.giveAsGermanDateTime(value=None,nvl='jetzt',secs=True) == time.strftime('%d.%m.%Y %H:%M:%S',time.localtime()))

print 'done'