import sys

sys.path.extend(['..'])

from checktype import Checktype
from dateconverter import Dateconverter

def hasException (code):
   """Prueft ob bei uebergebenen Code eine Exception auftritt"""

   retval = False
   try:
      eval(code)
   except:
      return True
   return False

class Person (Checktype):

   id                = 0
   name              = ''
   gehalt            = 0.0
   email             = ''
   groesseCm         = 0.0
   geburtsdatum      = None


   def errmsg(self,type,name,value):
      'Ausgabe Fehlermeldung'
      return "%(name)s ist kein %(type)s ('%(value)s')" % {'type':type,'name':name,'value':str(value)}

   def setValue(self,name,value):
      self.__dict__[name] = value
      
   def __setattr__(self,name,value):

      if name == 'id':
         if not self.isInteger(value): 
            raise ValueError(self.errmsg('int',name,value))
         else:
            self.setValue(name,value)

      elif name == 'name':
         if not self.isString(value) : 
            raise ValueError(self.errmsg('str',name,value))
         else:
            self.setValue('name',value)
        
      elif name == 'gehalt':
         if not self.isFloat(value) : 
            raise ValueError(self.errmsg('float',name,value))
         else:
            self.setValue(name,value)

      elif name == 'email':
         if not self.isEmail(value) : 
            raise ValueError(self.errmsg('email',name,value))
         else:
            self.setValue(name,value)

      elif name == 'groesseCm':
         if self.isInteger(value) or self.isFloat(value):
            self.setValue(name,value * 2.54)
         else:
            raise ValueError(self.errmsg('int/float',name,value))

      elif name == 'geburtsdatum':
         if self.isDate(value):
            dc = Dateconverter()
            self.setValue(name,dc.giveAsANSIDate(value))
         else:
            raise ValueError(self.errmsg('int/float',name,value))

      else:
         raise ValueError("'%(name)s' ist kein Attribut der Klasse %(classname)s" % {'name':name,'classname':self.__class__})


# ### Tests
#
person = Person()
assert(hasException("person.id='eins'"))
person.id=1
assert(hasException("person.id=1.2"))
assert(hasException("person.id='test@mail.com'"))

person.name = 'Pimpelhuber'
assert(hasException("person.name = 1"))
assert(hasException("person.name = 1.2"))
assert(hasException("person.id='test@mail.com'"))

assert(hasException("person.gehalt = 'Pimpelhuber'"))
assert(hasException("person.gehalt = 1"))
person.gehalt = 1.2
assert(hasException("person.gehalt='test@mail.com'"))

assert(hasException("person.email = 'Pimpelhuber'"))
assert(hasException("person.email = 1"))
assert(hasException("person.email = 1.2"))
assert(hasException("person.email='test@mail.com'"))

assert(hasException("person.groesseCm = 'Pimpelhuber'"))
person.groesseCm = 1
person.groesseCm = 1.2
assert(hasException("person.email='test@mail.com'"))

# Die Groesse wird in Zoll angegeben
person.groesseCm = 70 # 70 inch ~ 178cm
assert(str(person.groesseCm)+'cm' == '177.8cm')

person.groesseCm = 70.5
assert(hasException("person.groesseCm = 'Riese'"))
assert(hasException("person.groesseCm = 'test@mail.com'"))

assert(hasException("person.gibtesnicht = 'Monty'"))

person.geburtsdatum = '7.5.1957'
assert(person.geburtsdatum == '1957-05-07')
person.geburtsdatum = '1957-05-07'
person.geburtsdatum = '1957-05-07'
assert(hasException("person.geburtsdatum = '31.2.1957'"))


print 'done'