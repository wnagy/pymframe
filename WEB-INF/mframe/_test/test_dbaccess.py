# -*- coding: iso-8859-1 -*-

import sys
import os

sys.path.extend(['..','../..'])

from dbaccess.core import *

dbtype = 'sqlite'

def cvtResult(result):
   global dbtype
   if dbtype == 'sqlite': return result
   if dbtype == 'mysql': return result.replace('?','%s')

if dbtype == 'sqlite':
   testdb = Database('sqlite','test.db3')
elif dbtype == 'mysql':
   testdb = Database(dbtype,'localhost',3316,'root','','test')
elif dbtype == 'oracle':
   orc = {
      'username':'NORTHWIND',
      'password':'n0rthw1nd',
      'sid':'v9i',
      'host':'194.37.51.27',
      'port':'1521'
      }
   testdb = Database(dbtype,
      orc['username'],
      orc['password'],
      orc['sid'],
      orc['host'],
      orc['port']
      )

cursor = testdb.cursorFactory()



if dbtype == 'mysql':
   
   cursor.execute("""drop table if exists lov""")
   cursor.execute("""
   CREATE TABLE `lov` (
     `lovID` int(10) unsigned NOT NULL auto_increment primary key,
     `lovClass` varchar(32),
     `lovKey` varchar(64) default '',
     `lovValue` varchar(255) default '',
     `lovFlag1` varchar(255) default NULL,
     `lovFlag2` varchar(255) default NULL,
     `lovFlag3` varchar(255) default NULL,
     `lovFlag4` varchar(255) default NULL,
     `lovRemark` varchar(255) default NULL,
     `lovNumber` double default NULL,
     `lovDate`   datetime default NULL,
     `WHERE_TEST` varchar(255) default NULL,
     `lovTimeStamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
     `lovJson` varchar(1024)
     );
     """)
elif dbtype=='sqlite':   
   cursor.execute('drop table if exists lov')
   cursor.execute("""
   CREATE TABLE [lov] (
     [lovID] integer PRIMARY KEY AUTOINCREMENT,
     [lovClass] varchar(32),
     [lovKey] varchar(64),
     [lovValue] VARCHAR(255),
     [lovFlag1] varchar(255),
     [lovFlag2] varchar(255),
     [lovFlag3] varchar(255),
     [lovFlag4] varchar(255),
     [lovRemark] varchar(255),
     [lovNumber] Double,
     [lovDate] DATETIME,
     [WHERE_TEST] varchar(255)
     );
     """)

   cursor.execute('drop table if exists json')
   cursor.execute("""
   CREATE TABLE [json] (
     [jsoID] integer PRIMARY KEY AUTOINCREMENT,
     [jsoValue] varchar(32)
     );
     """)

elif dbtype=='oracle':
   try:
      cursor.execute('drop table lov')
   except: pass

   sql ="""
      CREATE TABLE lov (
        lovID integer,
        lovClass varchar2(32),
        lovKey varchar2(64),
        lovValue VARCHAR2(255),
        lovFlag1 varchar2(255),
        lovFlag2 varchar2(255),
        lovFlag3 varchar2(255),
        lovFlag4 varchar2(255),
        lovRemark varchar2(255),
        lovNumber NUMBER(10,2),
        lovDate DATE,
        WHERE_TEST varchar2(255),
        lovJson varchar(1024)
        )
        """   
   cursor.execute(sql)
   
cursor.execute("insert into lov (lovClass,lovKey,lovValue) values ('C1','1','eins')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue) values ('C1','2','zwei')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue) values ('C1','3','drei')")
cursor.close()

class LovDomain(Domain) :
   lovID          = None
   lovClass       = None
   lovKey         = None
   lovValue       = None
   lovFlag1       = None
   lovFlag2       = None
   lovFlag3       = None
   lovFlag4       = None
   lovRemark      = None
   lovDate        = None
   lovWhereTest   = None

   meta = {
      'tablename':'lov',
      'primarykey':'lovID',

      'fields':{
         'lovID'        : {'dbfield':'lovID',            'type':Database.TYPE_INTEGER},
         'lovClass'     : {'dbfield':'lovClass',         'type':Database.TYPE_STRING},
         'lovKey'       : {'dbfield':'lovKey',           'type':Database.TYPE_STRING},
         'lovValue'     : {'dbfield':'lovValue',         'type':Database.TYPE_STRING},
         'lovFlag1'     : {'dbfield':'lovFlag1',         'type':Database.TYPE_STRING},
         'lovFlag2'     : {'dbfield':'lovFlag2',         'type':Database.TYPE_STRING},
         'lovFlag3'     : {'dbfield':'lovFlag3',         'type':Database.TYPE_STRING},
         'lovFlag4'     : {'dbfield':'lovFlag4'}, # Absichtlich kein Typ
         'lovRemark'    : {'dbfield':'lovRemark',        'type':'Email'},
         'lovNumber'    : {'dbfield':'lovNumber',        'type':Database.TYPE_FLOAT},
         'lovDate'      : {'dbfield':'lovDate',          'type':Database.TYPE_ANSIDATE, 'secs':True},
         'lovWhereTest' : {'dbfield':'WHERE_TEST',       'type':Database.TYPE_STRING},
         }
      }
   
   def getLovValueUpper(self):
      return self.lovValue.upper()


class JsonDomain(Domain) :
   jsoID          = None
   jsoValue       = None
   meta = {
      'tablename':'json',
      'primarykey':'jsoID',

      'fields':{
         'jsoID'     : {'dbfield':'jsoID',            'type':'Integer'},
         'jsoValue'  : {'dbfield':'jsoValue',         'type':'Json'},
         }
   }

def hasException (code):
   """Prueft ob bei uebergebenen Code eine Exception auftritt"""

   retval = False
   try:
      eval(code)
   except Exception,e:
      return True
   return False


lov = LovDomain(testdb)
if dbtype == 'oracle':   
   #
   # BEI ORACLE DB FELDER UPPERCASE
   #
   for fld in lov.meta['fields']:
      value = lov.meta['fields'][fld]['dbfield']
      lov.meta['fields'][fld]['dbfield'] = value.upper()


# Pruefen ob None zugelassen wird (typecheckNoneAllowed = True
lov.lovID = None

# ### Test Typensichere Zuweisung
#

# None nicht erlaubt...
lov.typecheckNoneAllowed = False
assert(hasException('lov.lovID = None'))

# Integer
lov.lovID = 23

# Prufen ob ein Fehler auftritt
assert(hasException("lov.lovID = 'abc'"))
assert(hasException("lov.lovID = 23.42"))

assert(hasException("lov.lovRemark = 'test@nirgendwo.at'"))

assert(hasException("lov.lovRemark = 23.42"))
lov.lovClass = 'xxx'
lov.lovNumber = 23.42

assert(hasException("lov.lovNumber = 23"))

# Ohne Typepruefung
# Es darf kein Fehler auftreten
lov.lovFlag4 = 23

# Typenpruefung abschalten
lov.typecheckStrict = False
lov.lovID = 'abc'

# wieder einschalten
lov.typecheckStrict = True

#
# Klausel uebersetzung
#
lov.get(where= '$lovWhereTest is Null')
assert(lov.isOk)

lov.get(where= 'WHERE_TEST is Null')
assert(lov.isOk)

cnt = 0
for l in lov.eachDomain(where='$lovWhereTest is Null'): cnt += 1
assert(cnt==3)

# ### DB Checks...
#

# Test count
assert(lov.count()==3)
assert(lov.count(where="lovClass = 'C1' ") == 3)
assert(lov.count(where="lovValue = 'eins' ") == 1)

# Test Summenfunktion

assert(lov.sum('lovID') == 6)
assert(lov.sum('lovID',where="lovValue='drei'") == 3)

#test Min
assert(lov.min('lovID') == 1)
assert(lov.min('lovID',where="lovValue='drei'") == 3)

#test Max
assert(lov.max('lovID') == 3)
assert(lov.max('lovID',where="lovValue='drei'") == 3)

#test Avg
assert(lov.avg('lovID') == 2)
assert(lov.avg('lovID',where="lovValue='drei'") == 3)


cnt=0
for l in lov.eachDomain():
   cnt+=1
assert(cnt==3)


# Test eachDomain mit where
cnt = 0
for l in lov.eachDomain(where='lovKey=1'):
   cnt+=1
assert(cnt==1)

# Test eachDomain mit where
cnt = 0
for l in lov.eachDomain(where='lovClass = "C1"'):
   cnt+=1
assert(cnt==3)

# Test eachDomain mit orderby
cnt = 0
oldID = ''
for l in lov.eachDomain(orderby='lovValue'):
   if l.lovValue > oldID:
      cnt+=1
      oldID = l.lovValue
assert(cnt==3)


# Test: get mit PK
lov.get(1)
assert(lov.lovID == 1)


# test mit gefundemen key
lov.get(1)
assert lov.isOk


# Test: get mit where
lov.get(where="lovValue = 'zwei'")
assert(lov.lovValue=='zwei')


# Test: get mit where (isOk)
lov.get(where="lovValue = 'zwei'")
assert(lov.isOk)

# Test: get mit where (isOk)
lov.get(where="lovValue = '????'")
assert(not lov.isOk)

# Test notOK
lov.get(99)
assert (not lov.isOk)

# Test Domain Methode
lov.get(2)
assert(lov.getLovValueUpper()=='zwei'.upper())

# Test Loeschen aktueller Datensatz
lov.get(2)
lov.delete()
lov.get(2)
assert(not lov.isOk)

# Test delete in unbekannten Datensatz
lov.clear()
cnt = 0

assert(hasException('lov.delete()'))

# Test deleteAll
lov.deleteAll(where='lovID=3')
lov.get(3)
assert(not lov.isOk)

# Test clear
lov.get(1)
lov.clear()
assert(lov.lovID==None)

# Test Insert
lov.clear()
lov.lovClass = 'C2'
lov.lovKey   = 'k2'
lov.lovValue = 'v2'

lov.insert()
assert lov.isOk,str(lov.errors)+'\n'+lov.lastsql+'\n'+str(lov.lastsqlvalues)

lov.clear()
lov.get(4)
assert(lov.lovKey=='k2')

# Test Insert
lov.clear()
lov.lovClass = 'C2'
lov.lovKey   = 'k3'
lov.lovValue = 'v3'
lov.insert()
lov.clear()
lov.get(5)
assert(lov.lovKey=='k3')

# Test Update
lov.clear()
lov.get(5)
lov.lovFlag1='update'
lov.update()
lov.get(5)
assert(lov.lovFlag1=='update')

# Test: loesche aller Datensaetze
lov.deleteAll(where='(1=1)')
assert(lov.count() == 0)

# Test Datum
lov.clear()
lov.lovDate = '1.1.2011'
lov.insert()

lov.get(6)

assert lov.lovDate == '2011-01-01T00:00:00',lov.lovDate
assert(hasException("lov.lovDate = '31.2.2011'"))
assert(hasException("lov.lovDate = 'keindatum'"))

lov.clear()
lov.lovDate = '1.1.2011 10:22'
lov.insert()
lov.get(7)
assert(lov.lovDate == '2011-01-01T10:22:00')

# Pruefe log
if dbtype == 'mysql':   
   assert(lov.lastsql=='insert into lov (lovValue,WHERE_TEST,lovNumber,lovRemark,lovFlag2,lovKey,lovDate,lovFlag4,lovFlag3,lovClass,lovFlag1) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
   assert(str(lov.lastsqlvalues) == "[None, None, None, None, None, None, '2011-01-01T10:22:00', None, None, None, None]")

elif dbtype == 'sqlite':
   assert(lov.lastsql=='insert into lov (lovID,lovValue,WHERE_TEST,lovNumber,lovRemark,lovFlag2,lovKey,lovDate,lovFlag4,lovFlag3,lovClass,lovFlag1) values(?,?,?,?,?,?,?,?,?,?,?,?)')
   assert(str(lov.lastsqlvalues) == "[None, None, None, None, None, None, None, '2011-01-01T10:22:00', None, None, None, None]")

lov.lovDate = '31.12.2012 23:59'
lov.update()

if dbtype == 'mysql':   
   assert(lov.lastsql=="update lov set lovValue=%s,WHERE_TEST=%s,lovNumber=%s,lovRemark=%s,lovFlag2=%s,lovKey=%s,lovDate=%s,lovFlag4=%s,lovFlag3=%s,lovClass=%s,lovFlag1=%s where lovID=%s")
   assert(str(lov.lastsqlvalues) == "[None, None, None, None, None, None, '2012-12-31T23:59:00', None, None, None, None, 7L]")

elif dbtype == 'sqlite':
   assert(lov.lastsql=="update lov set lovID=?,lovValue=?,WHERE_TEST=?,lovNumber=?,lovRemark=?,lovFlag2=?,lovKey=?,lovDate=?,lovFlag4=?,lovFlag3=?,lovClass=?,lovFlag1=? where lovID = ?")
   assert(str(lov.lastsqlvalues) == "[7, None, None, None, None, None, None, '2012-12-31T23:59:00', None, None, None, None, 7]")

lov.delete()

if dbtype == 'mysql':   
   assert (lov.lastsql == 'delete from lov where lovID=%s')
elif dbtype == 'sqlite':   
   assert (lov.lastsql == 'delete from lov where lovID = ?')

assert(str(lov.lastsqlvalues) == '[]')

lov.deleteAll(where='1=1')
assert(lov.lastsql=='delete from lov where 1=1')
assert(str(lov.lastsqlvalues) == '[]')

#
# Testen eachDOmain mit limit Option
#
#

lov.clear()
for i in range(32):
   lov.lovKey = 'rec{0}'.format(i)
   lov.insert()

# Test auf Typensicherheit
assert(hasException("for l in lov.eachDomain(limit='x'): pass"))
assert(hasException("for l in lov.eachDomain(limit=123.2): pass"))
assert(hasException("for l in lov.eachDomain(limit=(1,3,3)): pass"))
assert(hasException("for l in lov.eachDomain(limit=('a',3)): pass"))
assert(hasException("for l in lov.eachDomain(limit=(1,'a')): pass"))
assert(hasException("for l in lov.eachDomain(limit=('ss','a')): pass"))
assert(hasException("for l in lov.eachDomain(limit=(1,)): pass"))
assert(hasException("for l in lov.eachDomain(limit=(,1)): pass"))

# Test 1 Datensatz
cnt = 0
for l in lov.eachDomain(limit=1): cnt=+1
assert(cnt==1)

# Test 16 Datensatz
cnt = 0
for l in lov.eachDomain(limit=16): cnt+=1
assert(cnt==16)

lstcheck = ['rec0','rec1','rec2']
result = []
for l in lov.eachDomain(limit=(0,3)): result.append(l.lovKey)

assert(lstcheck==result)
lstcheck.pop(0)
lstcheck.append('rec3')

result = []
for l in lov.eachDomain(limit=(1,3)):result.append(l.lovKey)
assert(lstcheck==result)

# Testen mit Ueberlauf
cnt = 0
for l in lov.eachDomain(limit=(30,99)): cnt+=1
assert(cnt==2)

# Testen offset mehr als gefordert
cnt=0
for l in lov.eachDomain(limit=100,where="lovKey > 'rec9'"): cnt += 1
assert(cnt==0)

cnt=0
for l in lov.eachDomain(limit=(100,10),where="lovKey like 'rec2'"): cnt += 1
assert(cnt==0)

# Test mit Where
cnt = 0

for l in lov.eachDomain(where='lovKey like "rec2%"',limit=5): cnt+=1
assert(cnt==5)

#
# Teste pseudorow rownum
cnt = 0
for l in lov.eachDomain(where='lovKey like "rec2%"',limit=5):
   cnt += 1
   assert(lov.getRownum() == cnt)

#
# rownum darf bei get nicht gesetzt sein
lov.get(1)


# Aufraeumen fuer nachste Tests
lov.deleteAll(where='(1=1)')

cursor = testdb.cursorFactory()
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C1','1','eins','A')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C1','2','zwei','B')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C1','3','drei','C')")
cursor.close()

#
# Testen deleteAll mit zu konvertierenden Klausel
#
cnt=0
for l in lov.eachDomain(where='$lovWhereTest is not Null'): cnt += 1
assert(cnt==3)

#
# Testen, wenn $ in Where vorkommt
#
cursor = testdb.cursorFactory()
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C1','1','eins','$A')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C2','2','zwei','$B')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C3','3','drei','$C')")
cursor.close()

cnt=0
for l in lov.eachDomain(where='$lovWhereTest = "$A"'): cnt += 1
assert(cnt==1)


#
# Testen orderby
#
cnt = 0
result = []
for l in lov.eachDomain(orderby='$lovWhereTest desc',where="$lovWhereTest like '$%'"): result.append(l.lovKey)
assert(result == ['3', '2', '1'])

lov.deleteAll(where="$lovWhereTest = 'B'")

lov.get(where="$lovWhereTest = 'B'")
assert(not lov.isOk)

lov.deleteAll(where="$lovWhereTest like '$%'")
cnt = 0
for l in lov.eachDomain(orderby='$lovWhereTest',where="$lovWhereTest like '$%'"): cnt += 1
assert(cnt==0)

# Aufraeumen fuer nachste Tests
lov.deleteAll(where='(1=1)')

#
# Pruefen filter Option in eachDomain
#
cursor = testdb.cursorFactory()
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C1','1','eins','$A')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C2','2','zwei','$B')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('C3','3','drei','$C')")
cursor.execute("insert into lov (lovClass,lovKey,lovValue,WHERE_TEST) values ('X1','4','vier','Viatmin C')")
cursor.close()
if dbtype == 'sqlite':
   result = 'lovID=? OR lovValue=? OR WHERE_TEST=? OR lovNumber=? OR lovRemark=? OR lovFlag2=? OR lovKey=? OR lovDate=? OR lovFlag4=? OR lovFlag3=? OR lovClass=? OR lovFlag1=?'
elif dbtype == 'mysql':
   result = 'lovID=%s OR lovValue=%s OR WHERE_TEST=%s OR lovNumber=%s OR lovRemark=%s OR lovFlag2=%s OR lovKey=%s OR lovDate=%s OR lovFlag4=%s OR lovFlag3=%s OR lovClass=%s OR lovFlag1=%s'

assert SqlConverter.handleFilterOption(lov,filter='')[0] == result

assert SqlConverter.handleFilterOption(lov,filter='')[0] == result

assert SqlConverter.handleFilterOption(lov,filter={'value':'','include':('*')})[0] == result
assert SqlConverter.handleFilterOption(lov,filter={'value':'','include':('$lovWhereTest','lovClass')})[0] == cvtResult('WHERE_TEST=? OR lovClass=?')

result = cvtResult('lovID=? OR lovValue=? OR lovNumber=? OR lovRemark=? OR lovFlag2=? OR lovKey=? OR lovDate=? OR lovFlag4=? OR lovFlag3=? OR lovClass=? OR lovFlag1=?')


assert  SqlConverter.handleFilterOption(lov,filter={'exclude':'$lovWhereTest'})[0] == result

result = cvtResult('lovID=? OR lovValue=? OR lovNumber=? OR lovRemark=? OR lovFlag2=? OR lovKey=? OR lovDate=? OR lovFlag4=? OR lovFlag3=? OR lovClass=?')
assert  SqlConverter.handleFilterOption(lov,filter={'exclude':['$lovWhereTest','lovFlag1']})[0] == result

result = cvtResult('lovID=:filter OR lovValue=:filter OR lovNumber=:filter OR lovRemark=:filter OR lovFlag2=:filter OR lovKey=:filter OR lovDate=:filter OR lovFlag4=:filter OR lovFlag3=:filter OR lovClass=:filter')
assert  SqlConverter.handleFilterOption(lov,filter={'exclude':['$lovWhereTest','lovFlag1']},dbtype='oracle')[0] == result

result = ['test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test']
assert SqlConverter.handleFilterOption(lov,filter={'value':'test','exclude':['$lovWhereTest','lovFlag1']})[1] == result

assert SqlConverter.handleFilterOption(lov,filter={'value':'test','exclude':['$lovWhereTest','lovFlag1']},dbtype='oracle')[1] == {'filter': 'test'}

assert SqlConverter.handleFilterOption(lov,filter={'value':'%1%','include':'lovClass'})[0] == cvtResult('lovClass like ?')
assert SqlConverter.handleFilterOption(lov,filter={'value':'%1%','include':'lovClass'})[1] == ['%1%']

#for l in lov.eachDomain():   print l.lovID,l.lovKey,l.lovClass
SqlConverter.setSelectAndValue(lov,listoption='count(*)',filter={'value':'%1%','include':'lovClass'})
assert(lov.lastsql==cvtResult('select count(*) from lov where (lovClass like ?)'))

assert(lov.count('lovKey in ("1","4")',filter={'value':'%1%','include':'lovClass'})==2)

#
# Nebenlauefige Pruefung: korrekte getRownum()
#
cnt = 0
for l in lov.eachDomain(filter='C%'): cnt += 1
assert cnt == 3 == lov.getRownum()

cnt = 0
for l in lov.eachDomain(filter='C_'): cnt += 1
assert cnt == 3 == lov.getRownum()

cnt = 0
for l in lov.eachDomain(filter='%C%'): cnt += 1
assert cnt == 4 == lov.getRownum()

cnt = 0
for l in lov.eachDomain(filter={'value':'%C','include':'$lovWhereTest'}): cnt += 1
assert cnt == 2 == lov.getRownum()

#
# Ueberpruefen ob where vor filter greift
#
cnt = 0
for l in lov.eachDomain(filter='C1',where='lovID=3'):cnt+=1
assert(cnt==0==lov.getRownum())

#
# Testen Filter, Where und Orderby
#
cnt = 0
for l in lov.eachDomain(
   where="$lovWhereTest='$C'",
   orderby='$lovWhereTest',
   filter={
      'value':'C_',
      'include':['lovClass','lovValue']
      }
   ):
   cnt+=1
assert lov.lastsql==cvtResult("select * from lov where (lovClass like ? OR lovValue like ?)  AND WHERE_TEST='$C'  order by WHERE_TEST")
assert cnt==1==lov.getRownum()


# Aufraeumen fuer nachste Tests
lov.deleteAll(where='(1=1)')

# 
# ** JSON **
# 
jso = JsonDomain(testdb)

jso.jsonEncoding = 'iso-8859-1'
jso.jsoID=99
jso.jsoValue = {'id':'A100',
                'value':{'f1':1,'f2':'Äpfel'}
                }
jso.insert()

jso.get(99)
assert jso.jsoValue['id'] == 'A100'
assert jso.jsoValue['value']['f1']==1
assert jso.jsoValue['value']['f2']==u'\u00C4pfel'
#print jso.jsoValue['value']['f2']

jso.jsonAsString = True
jso.get(99)
#print jso.jsoValue

print '[no errors dedected]'
