# -*- coding: utf-8 -*-
"""
Basismodul fuer alle Datenbakrelevaten Klassen.

HINT:
¯¯¯¯¯
   Die Klassen SqlConverter und EachDomain sind nicht dafuer gedacht
   direkt verwendet zu werden.

   Vorbereitet fuer
     + oracle
     + sqLite
     + mySql



History
¯¯¯¯¯¯¯
_VERSION_._AKTION____________________________________________________
2.2      | Verbesserung des Verhalten bei ORACLE DB
         |

"""

from dateconverter   import Dateconverter
from checktype       import Checktype
from conf.config     import Config
from datetime        import datetime
import re
import json
import codecs
import sys

__version__='2.2'

dbFieldIndex = lambda fieldnames,domain,fld : fieldnames.index(domain.meta['fields'][fld]['dbfield'])

class Database(object) :
   """
   Allgemeines Datenbank Objekt.
   """

   db = None
   filename = ''
   dbtype = None
   connectstring = None
   flds = []

   DBTYPE_ORACLE  = 'oracle'
   DBTYPE_SQLITE  = 'sqlite'
   DBTYPE_MYSQL   = 'mysql'

   TYPE_INTEGER   = 'Integer'
   TYPE_LONG      = 'Long'
   TYPE_DOUBLE    = 'Double'
   TYPE_STRING    = 'String'
   TYPE_FLOAT     = 'Float'
   TYPE_JSON      = 'Json'
   TYPE_EMAIL     = 'Email'
   TYPE_ANSIDATE  = 'AnsiDate'

   lastAutoincrement = None

   config         = Config()

   #
   # Fuer die Verwendung von JSON
   #
   jsonIndent = None             # wenn ungleich None, 
                                 # wird der Jsonstring formatiert gespeichert
   jsonAsString = False          # True: es wird keine Umwandlung in binaeres Format durchgefuehrt
                                 # False: Umwandlung der JsonString in binaraeres Format

   jsonEncoding =  "iso-8859-1"       # Speichern Coding


   def __init__(self,dbtype=None,*args) :
      """Initialisierung der Datenbank.

         @param dbtype    Fuer jede vorhanden Datenbank wird ein Type angegeben.
         @param args      Parameterliste:
                          fuer unterschiedliche Datenbanken werden unterschiedliche
                          Initialisierungstypen verwendet.
         """

      self.dbtype = dbtype
      config = Config()

      if dbtype == self.DBTYPE_SQLITE :
         from dbaccess.dbsqlite3 import DbSqlite3

         self.filename = args[0]
         self.db = DbSqlite3(args[0])

      elif dbtype == self.DBTYPE_ORACLE :
         # username, password, sid
         from dbaccess.dboracle import DbOracle
         nls_lang = config.oracle['nls_lang'] if 'nls_lang' in config.oracle else None
         if nls_lang is None:                        
            self.db = DbOracle(args[0],args[1],args[2],args[3],args[4])
         else:
            self.db = DbOracle(args[0],args[1],args[2],args[3],args[4],nls_lang)

         self.connectstring = self.db.connectstring

      elif dbtype == self.DBTYPE_MYSQL :
         from dbaccess.dbmysql import DbMySql
         self.db = DbMySql(args[0],args[1],args[2],args[3],args[4])
      else :
         raise "Ungueltiger Datenbanktype '%s'" % (dbtype)

   def cursorFactory(self):
      """
      Liefert eine Cursor auf die aktuelle Datenbank
      """
      return self.db.connection.cursor()

   def begin(self,mode='EXCLUSIVE'):
      """
      Startet eine Transaktion

      @param   mode        [DEFERED|IMMEDIATE|EXCLUSIVE] | EXCLUSIVE
      
      """
      if self.dbtype != self.DBTYPE_SQLITE : raise TypeError("Nur bei SQLite3 erlaubt")

      cur = self.db.connection.cursor()
      cur.execute('BEGIN {0} TRANSACTION'.format(mode))

   def commit(self):
      """
      Beendet fixierend eine Transaktion

      """
      if self.dbtype != self.DBTYPE_SQLITE : raise TypeError("Nur bei SQLite3 erlaubt")

      cur = self.db.connection.cursor()
      cur.execute('COMMIT TRANSACTION')

   def rollback(self):
      """
      Beendet rueckfuehrend eine Transaktion

      """
      if self.dbtype != self.DBTYPE_SQLITE : raise TypeError("Nur bei SQLite3 erlaubt")

      cur = self.db.connection.cursor()
      cur.execute('ROLLBACK TRANSACTION')

      

class Domain(Checktype) :
   """
   H I N T E R G R U N D
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

   Dient zur Verbindung der Domain mit einer Datenbanktabelle

   Eine Domain enthaelt
    + Die Felder welche von der Datenbanktabelle
      verwaltet werden sollen. Es ist nicht notwendig
      alle Felder zu deklarieren.
    + Eine Datenstruktur (metah) welche die Datenbanktabelle
      beschreibt und eine Verbindug zu den Domainfeldern deklariert.
    + Optional noch Methoden, welche zur Behandlung von Daten oder
      die Bereitstellung von ORM Methoden ermoeglichen.
    + HANDLER
        Handler liefern [True|False] Zurueck.
        Bei False wird die Datenbankaktion abgebrochen

        Fehlermeldungen koennen mit self.addError("Meldung")
        angegben werden.

   Typensichere Zuweisung
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
      Die Domain sichert sich gegen fehlerhafte Datentypenzuweisungen
      ab. Basierend auf den Angaben in der Mehtadaten Datenstruktur wird
      geprueft, ob die zugewiesene Datentypen den Datentypen in der Datenbanktabelle
      entsprechen.

   WESENTLICHE METHODEN
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

   insert
   ¯¯¯¯¯¯
      fuegt die Daten der Domai in die Datenbank ein.
      Beispiel:
        loc.clear()                 # Loeschen der Datenfelder der Domain
        lov.lovClass = 'Test'       # Befuellen
        lov.lovKey = '123'          # - " -
        lov.insert()                # In die Datenbank schreiben

   update
   ¯¯¯¯¯¯
      Aendert die Daten einer Datenbantabelle mit den in
      der Domain gespeicherten Daten.
      Beipiel:
         lov.get(12)                # Hole die Daten aus der Tabelle in die Domain
         lov.lovClass = 'TEST'      # Aender
         lov.update()               # in die Datebank schreiben

   delete
   ¯¯¯¯¯¯
      Loescht einen Datenbankeintrag basieren auf den
      in der Domain abgelegten Primary Key
      Beipiel:
         lov.get(13)                # Hole Datensatz
         lov.delete()               # Loesche den Datensatz aus Tabelle7

   get
   ¯¯¯
      Liest die Daten aus der Datenbank und kopiert diese
      in die Felder der Domain.
      Beispie:
         lov.get(where="lovKey = 'test' and lovClass = 'TEST'")
         if lov.isOK:
            print lov.lovID
         else:
            print 'Nicht gefunden'

   eachDomain
   ¯¯¯¯¯¯¯¯¯¯
      Serialisert die Domain. Basierend auf den Parametern werden
      alle oder eine Auswahl von Datensaetzen der Datenbankstabelle
      wird bereitgestellt.
      Die einfachste Form als Beispiel:

         for l in lov.eachDoamin():
            print l.lovKey

      where
         Where Klause
         Es kann entwede der original Tabellen Feldnamen oder
         der Domain Feldnamen mit vorangestellten Dollarzeichen ($) verwendet werden.

      orderby
         Order by Klausel
         Es koennen entwede der original Tabellen Feldnamen oder
         der Domain Feldnamen mit vorangestellten Dollarzeichen ($) verwendet werden.

      limit
         Kann ein Integer oder ein Tupple sein
         Wenn Integer wird maximal die Anzahl der genannten
         Datensaetze ausgegeben
         Bei einem Tupple wird vom angegebenen bis maximal
         bis zur angegenen Anzahl der Datensaetze ausgegeben.

      filter
          sucht in allen Datenbankfeldern nach dem
          uebergenen Wert.

          Ist Filter ein Dictionary koennen speziellere
          Einstellungen vorgenommen werden.
          Filter kann mit where kombiniert werden um das Suchergebnis weiter einzuschraenken.
          Beispiele:
              filter='Mayer'
                 es wird in allen Feldern nach dem Vorkommen 'Mayer' gesucht
              filter={'value':'Mayer',exclude=['PERSON_ID','GEHALT']}
                 Es wird in allen Feldern bis aus die Angegeben nach dem Filter gesucht
              filter={'value':'100',include=['$personID','$gehalt']}
                 es wird zuerst eine Ueberseetzung in Tabellenfeldnamen vogenommen und
                 nur in den angegebenen Feldern gesucht.

      cvtcharset
         wandelt nach dem lesen alle String Felder in den gewueschen charset um.
   """

   db                   = None         # Datenbank handle
   cursor               = None         # Cursor auf die Datenbanktabelle
   eachDomain           = None         # Objekthandle auf eachDomain
   tablename            = None         # Tabellename
   currec               = {}           # Aktueller Record
   isOk                 = False        # [True|False] Datenbankoperatonsstatus
   typecheckNoneAllowed = True         # True bei Typencheck ist None ein erlaubter Wert
   lastsql              = None         # Letzte verwendedete SQL Anweisung
   lastsqlvalues        = list()       # Liste der Werte fuer SQL
   typecheckStrict      = True         # False schaltet Typenueberpruefung ab
   errors               = []           # Liste von Fehlrmeldungen
   mode                 = None         # Haelt den Modus (delete,update,insert)
   hasErrors            = False        # Beim verarbeiten von mehreren Felder wird als
                                       # globale Fehlermelder verwendet.

   DELETE   = 'delete'
   UPDATE   = 'update'
   INSERT   = 'insert'
   includeflds = []
   def __init__(self,db=None,autocommit=True) :
      """
      Initialisierung der Domainklasse.

      @param         db          Datenkhandle

      """
      self.db = db
      if self.db is not None: self.isOk = True
      else: return
      self.clear()
      self.cursor = db.db.connection.cursor()

      # Autocommit nur bei mySQL
      if self.db.dbtype == self.db.DBTYPE_MYSQL:
         self.cursor.connection.autocommit(autocommit)

   def cvtCharset(self,fromCs='utf8', toCs='latin1'):
      """
      Umwandelt von characterset

      Versucht fuer alle Felde der Domain eine Umwandlung.

      @param   fromCs      von Characterset
      @param   toCs        zu Characterset

      """
      for fld in self.meta['fields'] :
         try:
            self.__dict__[fld] = self.__dict__[fld].decode(fromCs).encode(toCs) 
         except: pass


   def get(self,id=None,where=None,values=None):
      """
      Liest geanau einen Datensatz aus der Tabelle
      und kopiert die Daten in die Domain.

      HINT:
         wenn nicht gefunden wird isOk auf False gesetzt
         und die Datenfelder sind None.

      @param   id          Primary Key
      @param   where       Where Klausel
      @param   values      Inhaltswerte (Bei Verwendung von Platzhalten)

      """

      if id==None and where==None:
         raise ValueError("{0}::get: Keine Parameter angegeben".format(self.__class__.__name__))

      # bauen der Where-Klausel
      if where is not None:
         where = SqlConverter.convert(self,where)

      # Verwende Primariy Key fuer Datenbak
      primkey      = self.getDbPK()

      tablename   = self.meta['tablename']
      self.cursor = self.db.db.connection.cursor()

      # Wurde der Primary Key uebergeben
      if (id is not None):
         select = ''

         # Oracle Spezialbehandlung
         if self.db.dbtype == self.db.DBTYPE_ORACLE:

            select = "select * from %(tablename)s where %(pk)s=:id" % {'tablename':tablename,'pk':primkey}

            try:
               self.cursor.execute(select,{'id':id})
            except Exception,e:
               raise ValueError(str(e.message)+' errmsg: :'+select+' ID: '+str(id))

         # MySQL Spezialbehandlung
         elif self.db.dbtype == self.db.DBTYPE_MYSQL:
            select = "select * from %(tablename)s where %(pk)s=%%s" % {'tablename':tablename,'pk':primkey}
            self.cursor.execute(select,(id))

         else:
            select = "select * from %(tablename)s where %(pk)s=?" % {'tablename':tablename,'pk':primkey}
            self.cursor.execute(select,[id])

      else:
         if isinstance(where,str):
            if values is None:
               select = 'select * from %(tablename)s where %(where)s'% {'tablename':tablename,'where':where}
               self.cursor.execute(select)
            else:
               select = 'select * from %(tablename)s where %(where)s'% {'tablename':tablename,'where':where}               
               #print >>sys.stderr,"User prepared: {0} values {1}".format(select,','.join(values))
               self.cursor.execute(select,values)
         else:            
            raise Exception('where Option muss den Typ str oder dict haben!')
                     
      fieldnames = self.getFieldnames(self.cursor)

      record = self.cursor.fetchone()

      if record is not None:
         self.isOk = True
         for fld in self.meta['fields'] :
            iFieldnames = dbFieldIndex(fieldnames,self,fld)
            value = record[iFieldnames]
            if self.getDbFieldType(fld) == Database.TYPE_JSON and not self.db.jsonAsString:
               if value is not None:
                  value = json.loads(value,encoding=self.db.jsonEncoding)

            if self.db.dbtype == self.db.DBTYPE_MYSQL:
               fldType = self.getDbFieldType(fld)
               if fldType == Database.TYPE_ANSIDATE:
                  if value is not None:
                     value = value.isoformat()
            self.__dict__[fld] = value
            self.isOk = self.afterRead()         
      else:
         self.isOk = False

         for fld in self.meta['fields'] :
            self.__dict__[fld] = None
         self.afterRead()         
      return self.isOk

   def eachDomain(self,where=None,orderby=None,limit=None,filter=None) :
      """
      Iterator fuer jedes Vorkommen in der Datenbanktabelle.

      @param where      Where Klauses fuer die SQL Anwesung
      @param orderby    Sortierklausel
      @param limit      Limitiert Datensaetze
      @param filter     Filtert in allen Datenfeldern der Datenbank.

      usage
         for dom in domain.eachDomain() :
           print dom
      """

      self.db.rownum=0
      return EachDomain(self,where,orderby,limit,filter)

   def countRecords (self,where=None,orderby=None,limit=None,filter=None):
      """
      Liefert die Anzal von Domain
      """
      ed = EachDomain(self,where,orderby,limit,filter)

   def delete(self):
      """
      loescht aktuellen Datensatz

      HINT:
         vor dem Loeschen wird onDelete aufgerufen
         liefert die Methode False, so wird der Loeschvorgang
         abgebrochen

      @return  [True|Flase] das OK Kennzeichen

      """
      # Pruefen
      self.isOk = self.onDelete()
      if not self.isOk:
         return False

      self.isOk = self.onWrite(mode=self.DELETE)
      if not self.isOk: return False

      primkey     = self.getDbPK()
      tablename   = self.meta['tablename']
      self.cursor = self.db.db.connection.cursor()

      id = self.__dict__[self.getPK()]
      if id==None:
         raise Exception("Aktueller Datensatz hat keine Eintrag in %(primkey)s" % {'primkey':self.getPK()})

      if self.db.dbtype == self.db.DBTYPE_ORACLE:
         self.lastsql = "delete from %(tablename)s where %(primkey)s=:id" % {'tablename':tablename,'primkey':primkey}

      elif self.db.dbtype == self.db.DBTYPE_MYSQL:
         self.lastsql = "delete from %(tablename)s where %(primkey)s=%%s" % {'tablename':tablename,'primkey':primkey}

      else:
         self.lastsql = 'delete from %(tablename)s where %(primkey)s = ?' % {'tablename':tablename,'primkey':primkey}

      self.lastsqlvalues = list()
      if self.isOk:
         if self.db.dbtype == self.db.DBTYPE_ORACLE:
            self.cursor.execute(self.lastsql,{'id':id})
         elif self.db.dbtype == self.db.DBTYPE_MYSQL:
            self.cursor.execute(self.lastsql,(id))
         else:
            self.cursor.execute(self.lastsql,[id])
      else:pass
      return self.isOk

   def deleteAll(self,where=None):
      """
      Loeschen basierend auf einet Where Klausel

      HINT:
          Dieser Vorgang fueht keine Pruefung mit der Methode onDelete durch.

      @param   where    Eine where Klausel
                        Diese MUSS angegeben werden.

      """

      if where is None:
         raise Exception("bei delteAll ist Parameter where unbedingt notwendig")

      where = SqlConverter.convert(self,where)

      tablename   = self.meta['tablename']
      self.cursor = self.db.db.connection.cursor()
      self.lastsqlvalues = list()
      self.lastsql = "delete from %(tablename)s where %(where)s" % {'tablename':tablename,'where':where}
      self.cursor.execute(self.lastsql)

   def update(self,usedFields=None):
      """
      Veraendern des Datensatzes basieren auf den Inhalten der Domain
         HINT:
            vor dem Update wird die Methode onUpdate aufgerufen.
            Liefert diese False zurueck wird der Ueberschreibenvorgang
            abgebrochen.

            Der Methode kann eine Feldliste uebergeben werden.
            Ist diese deklariert, so werden nur die deklarierten Felder
            zum Update verwendet.

      @return  [True|Flase] das OK Kennzeichen

      """
     
      self.isOk = self.onUpdate()
      if not self.isOk: return False

      self.isOk = self.onWrite(mode=self.UPDATE)
      if not self.isOk: return False
         
      flds = list()

      if usedFields is not None:
         flds = usedFields
      else:
         for fld in self.meta['fields'].keys():
            flds.append(fld)
         
      # Included Flds
      flds += self.includeflds
               
      values = list()
      primkey     = self.getPK()

      # Sicherheitsabfrage:
      # Bei Update muss Primary Key Feld vorhanden sein.
      #
      if not primkey in flds:
         raise Exception('Bei update konnte der Primary Key "{0}" in Feldliste [{1}] nicht gefunden werden'.format(primkey,','.join(flds)))

      for fld in flds:
         if self.__dict__[fld] is None:
            values.append(None)
         else:
            values.append(self.__dict__[fld])

      tablename   = self.meta['tablename']
      values.append(self.__dict__[primkey])
      self.lastsqlvalues = values

      if self.db.dbtype == self.db.DBTYPE_ORACLE:
         
         # Erzeugen Oracle spezialisertes Update Statement
         from dbaccess.dboracle import DbOracle
         dbFlds = []
         self.lastsqlvalues = {}
         
         for fld in flds:
            dbFlds.append(self.getDbFieldName(fld))
            self.lastsqlvalues[self.getDbFieldName(fld)] = self.__dict__[fld]

         self.lastsql = DbOracle.giveUpdate(
             tablename=tablename,
             fields=dbFlds,
             primarykey=self.getDbPK()
             )

      elif self.db.dbtype == self.db.DBTYPE_MYSQL:
         # Erzeugen Mysql spezialisertes Insert Statement
         from dbaccess.dbmysql import DbMySql
         dbFlds = []
         self.lastsqlvalues = []
         for fld in flds:
            if fld != self.getPK():
               dbFlds.append(self.getDbFieldName(fld))
               self.lastsqlvalues.append(self.getValue(fld))
         self.lastsqlvalues.append(self.getValue(self.getPK()))

         self.lastsql = DbMySql.giveUpdate(
             tablename=tablename,
             fields=dbFlds,
             primarykey=self.getDbPK()
             )

      else:
         fragezeichen = '?,' * len(flds)
         fragezeichen = fragezeichen[:-1]

         fldList = list()

         for fld in flds:
            fldList.append('%(fld)s=?' % {'fld':self.getDbFieldName(fld)})
         self.lastsql = 'update %(tablename)s set %(flds)s where %(primkey)s = ?' % {
            'tablename':tablename,
            'flds':','.join(fldList),
            'primkey':self.getDbPK()
            }

      if self.isOk:
         try:
            self.cursor.execute(self.lastsql,self.lastsqlvalues)
         except Exception,e:
            self.isOk = False
            self.errors.append("DB Fehler bei update {0} sql: {1}".format(e,self.lastsql))
         
      return self.isOk

   def createSqlParameter(self):
      self.lastsqlvalues = []
      self.flds =[]
      
      for fld in self.meta['fields'].keys():
         if not isinstance(fld,str) :
            raise ValueError("Felder in Domain muessen als Strings deklariert werden!")

         dbFieldName = self.getDbFieldName(fld)

         if self.db.dbtype == self.db.DBTYPE_MYSQL:
            if dbFieldName != self.getDbPK():
               self.flds.append(dbFieldName)
               if self.__dict__[fld] is None:
                  self.lastsqlvalues.append(None)
               else:
                  self.lastsqlvalues.append(self.__dict__[fld])
         elif self.db.dbtype == self.db.DBTYPE_SQLITE:
            self.flds.append(dbFieldName)
            if self.__dict__[fld] is None:
               self.lastsqlvalues.append(None)
            else:
               self.lastsqlvalues.append(self.__dict__[fld])

         elif self.db.dbtype == self.db.DBTYPE_ORACLE:
            self.flds.append(dbFieldName)
            if self.__dict__[fld] is None:
               self.lastsqlvalues.append(None)
            else:
               self.lastsqlvalues.append(self.__dict__[fld])

            
         else:
            raise Exception('Ungueltiger dbtype: "{0}"'.format(self.db.dbtype))      

   def insert(self):
      """
      Einfuegen eines Datensatzes
      Die aktuellen Werte aus der Domain werden in
      die Datenbank geschrieben.

      HINT:
         vor dem Insert wird die Methode onInsert aufgerufen.
         Liefert diese False zurueck wird der Einfuegevorgang
         abgebrochen.

      @return  [True|Flase] das OK Kennzeichen
      """
      
      self.isOk = self.onInsert()
      if not self.isOk: return False

      self.isOk = self.onWrite(mode=self.INSERT)
      if not self.isOk: return False


      values = list()

      tablename   = self.meta['tablename']
      
      self.lastsqlvalues = values
      
      if self.db.dbtype == self.db.DBTYPE_ORACLE:
         # Erzeugen Oracle spezialisertes Insert Statement
         from dbaccess.dboracle import DbOracle         
         
         self.createSqlParameter()

         self.lastsql = DbOracle.giveInsert(tablename=tablename,fields=self.flds)
                  
      elif self.db.dbtype == self.db.DBTYPE_MYSQL:
         from dbaccess.dbmysql import DbMySql
         
         self.createSqlParameter()
         
         self.lastsql = DbMySql.giveInsert(tablename=tablename,fields=self.flds,primarykey=self.getDbPK())
         self.lastsqlvalues = tuple(self.lastsqlvalues)

      else:
         # Herstellen einer Liste von Fragezeichen
         # fuer prepared statement
         self.createSqlParameter()
         fragezeichen = '?,' * len(self.flds)
         fragezeichen = fragezeichen[:-1]
         self.lastsql = 'insert into %(tablename)s (%(flds)s) values(%(fragezeichen)s)' % {
            'tablename':tablename,
            'flds':','.join(self.flds),
            'fragezeichen':fragezeichen}


      if self.isOk:
         self.createSqlParameter()
         try:
            self.cursor.execute(self.lastsql,self.lastsqlvalues)
         except Exception,e:
            self.isOk = False
            self.errors.append("DB Fehler bei insert {0}".format(e))

      if self.isOk and self.db.dbtype == self.db.DBTYPE_SQLITE:
         sql = 'select seq from sqlite_sequence where name="{0}"'.format(tablename)
         self.cursor.execute(sql)
         next_record = self.cursor.fetchone()

         # Pruefen ob last Autoincrement erreichbar
         # ist wenn nicht wird None gespeichert.
         if next_record is None:
            self.lastAutoincrement = None
         else:
            self.lastAutoincrement = next_record[0]

      elif self.isOk and self.db.dbtype == self.db.DBTYPE_MYSQL:
         self.cursor.execute('SELECT last_insert_id();')
         next_record = self.cursor.fetchone()
         self.lastAutoincrement = next_record[0]
      else:
         self.lastAutoincrement = None

      return self.isOk


   def count(self,where=None,filter=None):
      """
      Liefert die Anzahl der Datensaetze ggf. basierend auf where

      @param   where    Where Klausel

      @return  Wert oder None
      """
      SqlConverter.setSelectAndValue(self,where=where,filter=filter,listoption='count(*)')
      self.cursor.execute(self.lastsql,self.lastsqlvalues)

      record = self.cursor.fetchone()
      return record[0]


   def sum(self,fld,where=None):
      """
      Liefert die Summenfunktion ggf. basierend auf where

      @param   where    Where Klausel

      @return  Wert oder None
      """
      tablename   = self.meta['tablename']

      select = 'select sum(%(fld)s) from %(tablename)s' % {'tablename':tablename,'fld':fld}
      if where is None:
         self.cursor.execute(select)
      else:
         self.cursor.execute(select+' where %(where)s' % {'where':where})

      record = self.cursor.fetchone()
      return record[0]

   def min(self,fld,where=None):
      """
      Liefert die Summenfunktion ggf. basierend auf where

      @param   where    Where Klausel

      @return  Wert oder None

      """
      tablename   = self.meta['tablename']

      select = 'select min(%(fld)s) from %(tablename)s' % {'tablename':tablename,'fld':fld}
      if where is None:
         self.cursor.execute(select)
      else:
         self.cursor.execute(select+' where %(where)s' % {'where':where})

      record = self.cursor.fetchone()
      return record[0]

   def max(self,fld,where=None):
      """
      Liefert die Summenfunktion ggf. basierend auf where

      @param   where    Where Klausel

      @return  Wert oder None
      """
      tablename   = self.meta['tablename']

      select = 'select max(%(fld)s) from %(tablename)s' % {'tablename':tablename,'fld':fld}
      if where is None:
         self.cursor.execute(select)
      else:
         self.cursor.execute(select+' where %(where)s' % {'where':where})

      record = self.cursor.fetchone()
      return record[0]

   def avg(self,fld,where=None):
      """
      Liefert die Summenfunktion ggf. basierend auf where

      @param   where    Where Klausel

      @return  Wert oder None
      """
      tablename   = self.meta['tablename']

      select = 'select avg(%(fld)s) from %(tablename)s' % {'tablename':tablename,'fld':fld}
      if where is None:
         self.cursor.execute(select)
      else:
         self.cursor.execute(select+' where %(where)s' % {'where':where})

      record = self.cursor.fetchone()
      return record[0]

   def writedb(self,cgiparam=None,flash=None,action=None,id=None):
      """
      Behandelt alle schreibenden Datenbankoperationen.
      Die Methode verwendet eine "Upsert" Strategie.
      Wird der Datensatz basierdend auf seinem Primary-Keys
      gefunden wird eine update sonst ein insert Anweisung generiert.

      Tritt ein Fehler auf, wird False zurueckgeliefert

      @param   cgiparam    Funktion zur Bearbeitung des CGI
      @param   flash       Funktion um Nachrichten an das GUI zu uebermitteln
      @param   action      'delete': Der Datensatz wird geloescht
      @param   id          Primary Key
      """
      if cgiparam is None:
         raise Exception("bei writedb muss cgiparam uebergeben werden")

      if flash is None:
         raise Exception("bei writedb muss flash uebergeben werden")

      retval = True
      self.isOk = True

      if action == 'delete':

         self.mode = self.DELETE

         if id is None:
            id = cgiparam(name='id', nvl='')
         else:
            id = cgiparam(name=id,nvl='')
         if id == '': return

         self.get(id)

         if self.isOk:
            self.isOk = self.delete()


         return self.isOk

      elif action != 'save':
         raise Exception("Bei Methode dbwrite: im Parameter action sind nur 'delete' und 'save' gueltig. Inhalt:'{0}'".format(action))

      if id is None:
         id = cgiparam(name='id',nvl='')
      else:
         id = cgiparam(name=id,nvl='')

      if id == '':
         self.mode = self.INSERT
         self.fromCgi(cgiparam)

         if self.isOk:
            idfld = self.getPK()
            cmd = "self.{0} = None".format(idfld)
            exec cmd
            retval = self.insert()
         else:
            flash('<br />'.join(self.errors))
            retval = False
      else:
         # Pruefen ob Insert oder Update notwendig
         idfld = self.getDbPK()

         self.cursor = self.db.db.connection.cursor()
         if self.db.dbtype == self.db.DBTYPE_ORACLE:
            select = "select * from {0} where {1}=:1".format(self.meta['tablename'],idfld)
            self.cursor.execute(select,[id])
         elif self.db.dbtype == self.db.DBTYPE_MYSQL:
            select = "select * from %(tablename)s where %(idfld)s=%%s" % {'tablename':self.meta['tablename'],'idfld':idfld}
            self.cursor.execute(select,(id))
         else:
            select = "select * from {0} where {1}=?".format(self.meta['tablename'],idfld)
            self.cursor.execute(select,[id])

         if self.cursor.fetchone() is not None:
            self.mode = self.UPDATE
         else:
            self.mode = self.INSERT

         self.fromCgi(cgiparam)
         
         if self.isOk:
            if self.mode == self.UPDATE:
               self.isOk = self.update(self.usedFields(cgiparam))
            else:
               self.isOk = self.insert()

            if not self.isOk:
               flash('<br />'.join(self.errors))
               retval = False

         else:
            flash('<br />'.join(self.errors))
            retval = False

      return retval

   """
   === H A N D L E R ===

   HINT:
      Handler liefern [True|False] Zurueck.
      Bei False wird die Datenbankaktion abgebrochen

      Fehlermeldungen koennen mit self.addError("Meldung")
      angegben werden.
   """

   def onReadFromCgi(self,fieldname,value):
      """
      Veraender eines eingelesenen Wertes

      @param fieldname         Feldname
      @param value             Inhalt aus dem CGI

      @return  Veraendertet Inhalt aus dem CGI
      """
      return value


   def onCgiField(self,fieldname,value):
      """
      Wenn die Domain ueber das CGI befuellt wir
      wird bei jedem Feld dieser Handler aufgerufen.


      @param fieldname         Feldname
      @param value             Inhalt aus dem CGI

      @param [True|False]      wird False uebergeben so bricht das Laden ab
      """
      return True

   def afterCgi(self):
      """
      Wird nach dem Einlesen aller Felder aus dem CGI
      aufgerufen.

      @return  [True|False]
      """
      return True

   def onDelete(self):
      """
      Wird aufgerufen vor Loeschen eines Datensatzens

      @return [True|False]
      """         
      return True

   def onInsert(self):
      """
      Wird aufgerufen vor Einfuegen eines Datensatzens
      False beendet die Aktion

      @return [True|False]

      """
      return True

   def onUpdate(self):
      """
      Wird aufgerufen vor Veraendern eines Datensatzens
      False beendet die Aktion

      @return [True|False]

      """
      return True

   def onWrite(self,mode=None):
      """
      Wird vor jeder schreibenden
      Operation aufgerfuen.

      @param  mode     Enthaelt insert/update/delete

      @return [True|False]

      """
      return True

   def afterRead(self):
      """
      wird nach dem Lesen einer Doman aufgerufen

      @return [True|False] 
      """         
      return True

   #
   # ################# END OF HANDLER


   def addError(self,msg=''):
      """
      Erweitert die Fehlermeldungsliste um
      die uebergebene Meldung

      @param  msg         Fehlermeldung

      """
      self.errors.append(msg)


   def getRownum(self):
      """
      Liefert die pseudospalte rownum bei eachDomain.
      Diese Methode kann dafuer verwendet werden um zu pruefen,
      ob die eachDomain Methode daten geliefert hat.
      """
      return self.db.rownum

   def raiseTypeError(self,fldtype,name,value):
      """
      gibt Fehlermeldung bei Typenfehler aus.

      HINT:
         Diese Methode wirft eine TypeError mit
         einer Fehlermeldung

      @param   fldtype        Typ des Feldes
      @param   name           Domain-Feldname
      @param   value          Uebergebener Wert

      """
      myType =  str(type(value))
      raise TypeError('"%(value)s" ist nicht vom Typ %(type)s in Feld %(name)s, Typ: %(mytype)s in Klasse: "(%(classname)s)"' % {'value':str(value),'type':fldtype,'name':name,'classname':self.__class__,'mytype':myType})

   def getDomainFieldNames(self):
      """
      Liefert eine Liste mit den Domainfeldern
      """
      retval = []
      for fld in self.meta['fields'].keys():
         retval.append(fld)

      return retval


   def __setattr__(self,name,value):
      """
      Pruefen auf Typengueltigkeit.

      HINT:
         geht die Pruefung fehl, so wird ein
         Fehler geworfen.

      @param   name        Domainfeldname
      @param   value       Wert

      """

      dc = Dateconverter()

      # Wurde Typenueberpruefung abgeschalten
      if not self.typecheckStrict:
         self.__dict__[name] = value
         return

      # None als Eingabewert erlaubt.
      if self.typecheckNoneAllowed and value is None:
         self.__dict__[name] = value
         return

      # Ist das ein Domainfeld
      if name in self.meta['fields']:
         # Feldobjekt
         fld = self.meta['fields'][name]
         # Wurde type in meta deklariert
         if 'type' in fld:
            # Integer pruefen
            if fld['type'] == Database.TYPE_INTEGER:
               if self.isInteger(value):
                  self.__dict__[name] = value
               else:
                  self.raiseTypeError(fld['type'],name,value)
            elif fld['type'] == Database.TYPE_LONG:
               if self.isLong(value):
                  self.__dict__[name] = value
               else:
                  self.raiseTypeError(fld['type'],name,value)

            # String pruefen
            elif fld['type'] == Database.TYPE_STRING:
               if self.isString(value):
                  self.__dict__[name] = value
               else:
                  self.raiseTypeError(fld['type'],name,value)

            # Emailadresse pruefen
            elif fld['type'] == Database.TYPE_EMAIL:
               if self.isString(value):
                  self.__dict__[name] = value
               else:
                  self.raiseTypeError(fld['type'],name,value)

            # Float
            elif fld['type'] == Database.TYPE_FLOAT:
               if self.isFloat(value):
                  self.__dict__[name] = value
               else:
                  self.raiseTypeError(fld['type'],name,value)

            # Database.TYPE_DOUBLE ist equivalent zu float
            elif fld['type'] == Database.TYPE_DOUBLE:
               if self.isFloat(value):
                  self.__dict__[name] = value
               else:
                  self.raiseTypeError(fld['type'],name,value)

            # JSON
            elif fld['type'] == Database.TYPE_JSON:               
               self.__dict__[name] = json.dumps(value,indent=self.db.jsonIndent,encoding=self.db.jsonEncoding)                              
            
            # Behandlung des Datentypes Date.
            # Dieser wird nur 
            elif fld['type'] == 'Date':
               if self.db.dbtype == self.db.DBTYPE_ORACLE:                  
                  
                  # Ist Value schon ein Zeitobjekt ist
                  # keine Umwandlung mehr notwendig.
                  if isinstance(value,datetime): 
                     self.__dict__[name] = value
                     return
                     
                  try:
                     value = dc.fromString(value)
                  except:
                     self.raiseTypeError(fld['type'],name,value)
               
                  value =  datetime.strptime(value, "%Y-%m-%dT%H:%M")

                  self.__dict__[name] = value
               elif self.db.dbtype in [self.db.DBTYPE_SQLITE,self.db.DBTYPE_MYSQL]:
                  if self.isDate(value):
                     dc = Dateconverter()
                     secs = True
                     if 'secs' in fld: secs = fld['secs']
                     self.__dict__[name] = dc.giveAsANSIDateTime(value,secs=secs)
                  else:
                     self.raiseTypeError(fld['type'],name,value)                  
               else:
                  raise Exception("Ungueltiger Datenbanktyp")
                  return

            # AnsiDate
            # In der Domain kann die Option secs (True/False) angegeben werden
            # diese steuert ob Sekunden angegeben werden sollen.

            elif fld['type'] == Database.TYPE_ANSIDATE:
               if self.isDate(value):
                  dc = Dateconverter()
                  secs = True
                  if 'secs' in fld: secs = fld['secs']
                  self.__dict__[name] = dc.giveAsANSIDateTime(value,secs=secs)
               else:
                  self.raiseTypeError(fld['type'],name,value)

            else:
               raise Exception("Ungueltiger Type '{0} in Feld {1}".format(fld['type'],name))
               return
         else:
            pass

      else:
         self.__dict__[name] = value

   def getFieldnames(self,cursor) :
      """
      Liefert eine Liste mit Datenbank-Feldname fuer den Cursor.

      @param   cursor      Cursor auf eine Datenbanktabelle

      """
      lstField = []

      for item in cursor.description :
         lstField.append(item[0])

      return lstField

   def set(self,name=None,value=None):
      """
      Setzt den Inhalt eines Feldes der Domain

      @param   name        Domainfeldnamen
      @param   value       zu setzender Wert

      """
      if name is None:
         raise ValueError("Domain:: Feldname fehlt")
      self.__setattr__(name,value)

   def clear(self):
      """
      setzt alle Attribute welche als Datenbankfelder deklariert
      wurden auf None.

      Diese Method kann dazu verwenden werden das Domain-Objekt
      wiederzuverwenden.
      """
      for fld in self.meta['fields'].keys():
         self.__dict__[fld] = None


   def getPK(self):
      """
      Gibt den Domain-Felnamen des Primary Keys zurueck
      """
      return self.meta['primarykey']

   def getDbPK(self):
      """
      Gibt den Namen des Primary Key der Datenbanktabelle zurueck.
      """
      pk = self.meta['primarykey']

      return self.meta['fields'][pk]['dbfield']

   def getDbFieldName(self,fld):
      """
      Liefert den Namen des Datenbankfeldes auf basis des Domainfeldnamen

      @param   fld         Domainfeldname

      @return  Datenbankfeldname
      """
      return self.meta['fields'][fld]['dbfield']

   def getDbFieldType(self,fld):
      """
      Liefert den Type des Datenbankfeldes auf basis des Domainfeldnamen

      @param   fld         Domainfeldname

      @return  Typ
      """
      try:
         return self.meta['fields'][fld]['type']
      except:
         return Database.TYPE_STRING

   def getDbFieldNames(self):
      """
      Liefert eine Liste mit allen Tabellenfeldnamen

      @return     Liste der Namen
      """

      retval = []
      for fld in self.getDomainFieldNames():
         retval.append(self.getDbFieldName(fld))
      return retval

   def usedFields(self,cgiparam=None):
      """
      Liefert eine Liste von Feldnamen,
      welche durch das CGI uebergeben wurden
      und in der Domain Feldliste vorhanden ist.

      @param cgiparam     Methode zum lesen aus dem CGI

      @return Feldlist
      """
      if cgiparam is None:
         raise Exception("Die Methode fromCgi muss cigparam uebergeben werden")
      flds = []

      for fld in self.meta['fields'].keys():
         value = cgiparam(name=fld,nvl='',noneifnotused=True)
         if value is not None:
            flds.append(fld)

      return flds

   def prepareValue(self,fld,value):
      """
      Umwandlung einer String Variable in die von der Domain
      gewuenschten Datentyp

      usage: prepareValue (fld,value)
      
      @param fld          Feldname
      @param value        Inhalt

      @return              Praeparierter Inhalt

      HINT:
         Wenn Ein Fehler auftritt, wird self.hasErrors gesetzt

      """

      # Soll der Eingelesenen Wert aus dem CGI
      # veraendert werden?
      value = self.onReadFromCgi(fieldname=fld,value=value)

      # Pruefen ob Checkroutine verwendet werden soll
      self.isOk = self.onCgiField(fieldname=fld,value=value)

      if not self.isOk: self.hasErrors = True
      # Ein Leeres Feld wird als None behandelt
      if re.search('^\s*$',value):
         value = None

      try:
         if value is not None:
            fldtype = self.meta['fields'][fld]['type']
            if fldtype == Database.TYPE_INTEGER:
               value = int(value)
            elif fldtype == Database.TYPE_DOUBLE:
               value = value.replace(',','.')
               value = float(value)

####            self.set(fld,value)
      except Exception,e:
         self.hasErrors = True
         self.errors.append('%(fld)s hat einen ung&uuml;ltigen Wert: "%(value)s %(msg)s" ' % {'fld':fld,'value':value,'msg':e.message})
      return (value)

   def fromCgi(self,cgiparam=None,flds=None,typecheckStrict=True):
      """
      Befuellen der Domain aus dem CGI
      HINT:
         Typecheck wird ausgeschalten!
         wirft eine Exception, wenn ein Fehler beim befuellen auftritt

      @param cgiparam     Methode zum lesen aus dem CGI
      @param flds         eine Liste von Felder, welche verewendet werden soll
                              ist die Liste None, so wird die Feldliste aus den Metadaten uebernommen

      @return  [True|Flase] das OK Kennzeichen
      """
      self.typecheckStrict = typecheckStrict
      
      if cgiparam is None:
         raise Exception("Die Methode fromCgi muss cigparam uebergeben werden")

      self.isOk = True

      if flds is None:
         flds = self.usedFields(cgiparam)

      self.hasErrors = False

      for fld in flds:
         value = cgiparam(name=fld,nvl=None)
         value = self.prepareValue(fld,value)
         try:
            self.set(fld,value)
         except Exception,ex:
            self.hasErrors = True
            self.errors.append(str(ex))

      # Wenn bislang noch keine Fehler aufgetreten sind
      # wird handler afterCgi auferufen.
      if not self.hasErrors:
         self.hasErrors = not self.afterCgi()

      if self.hasErrors:
         self.isOk = False

      return self.isOk

   def getDomain(self,where=None) :
      """
      Gibt genau eine Domain oder None zurueck, wenn nicht gefunden.

      @param   where       Whereklausel
      """

      getDomain = GetDomain(self)
      getDomain.get(self,where)

   def getValue(self,fld):
      """
      Liefert den Inhalt eines Feldes auf Grund eines Domain-Feldnamen

      @param fld           Feldnamen

      """
      value = None
      exec('value = self.%(fld)s' % {'fld':fld})
      return value


   def __del__(self):
      pass
      #self.db.db.connection.commit()


class EachDomain() :
   """
   Durchlaufen eines Datenbankstroms.
   Optional koennen bei der Instanzierung eine Kriterien und eine
   Sortierung kodieren.

   Die Daten werden nach dem Lesen in die Domaifelder
   kopiert.

   HINT:
      Diese Klasse wird von der Domain-Klasse verwenden und
      soll nie direkt verwendet werden.

   Usage:
         for lovDom in lov.eachDomain(where='lovID=23','lovClass')
            print lovDom

   """

   db       = None
   cursor   = None
   domain   = None
   limit    = None
   offset   = None
   rownum   = None


   def __init__(self,domain,where=None,orderby=None,limit=None,filter=None) :
      """
      Iteration ueber Domain initialisieren

      @param domain     Domainobjekt
      @param where      where Klausel fuer SQL Anweisung
      @param orderby    Sortierklausel
      @param limit      Limit Klausel
                        Limit kann ein Integer oder
                        ein Tuple mit zwei Elementen uebergeben werden.
                        Limit mit INteger liefert bis zu der angegebenen Meng
                        von Datensaetzen.
                        Limit mit Tuppel ueberliest die anzahl von Datensaetzen in
                        Element 1 und gibt maximal die Anzahl der Daensaetze im 2. Element zurueck.
      """
      self.domain = domain
      
      self.cursor = domain.db.db.connection.cursor()

      # Where by Mysql alle % durch %% ersetzen,
      # da sonst Probleme mit prepared statments
      if where is not None:
         if domain.db.dbtype == domain.db.DBTYPE_MYSQL:
            where = where.replace('%','%%')
      #
      # Behandlung von Limt
      #
      if limit is not None:

         if isinstance(limit,int):
            self.offset = 0
            self.limit  = limit
         elif isinstance(limit,tuple):
            if len(limit) != 2: raise Exception("eachDomain, muss genau zwei Elemente haben")
            self.offset = int(limit[0])
            self.limit  = int(limit[1])
         else:
            raise Exception("eachDomian bei Option limit nur Integer oder Tuple gueltig")

      SqlConverter.setSelectAndValue(domain,where,filter,orderby)

      self.cursor.execute(domain.lastsql,domain.lastsqlvalues)
      
      self.value = None

      # Wenn offset deklariert, Datensaetze ueberlesen
      self.rownum = 0
      if self.offset is not None:
         for cnt in range(self.offset):
            record = self.cursor.fetchone()
            if record is None: self.rownum+=1

   def __iter__(self) :
      """
      Gibt Iterator zurueck.
      """
      return self

   def next(self) :
      """
      durchlaufen des Datenstromes bis keine
      weiteren Datensaetze mehr gefunden werden.
      """

      record = self.cursor.fetchone()

      if record is None :
        raise StopIteration
      self.rownum += 1

      if self.limit is not None:
         if self.rownum > self.limit:
            raise StopIteration


      fieldnames = self.domain.getFieldnames(self.cursor)
            
      for fld in self.domain.meta['fields'] :
         try:
            iFieldnames  = dbFieldIndex(fieldnames,self.domain,fld)
         except Exception,e:
            raise(ValueError(e.message+', Index: "'+fld+'"'))

         value = record[iFieldnames]
         
         if self.domain.getDbFieldType(fld) == Database.TYPE_JSON and not self.domain.db.jsonAsString:
            if value is not None:
               value = json.loads(value,encoding=self.domain.db.jsonEncoding)
               
         if self.domain.db.dbtype == self.domain.db.DBTYPE_MYSQL:
            fldType = self.domain.getDbFieldType(fld)
            if fldType == Database.TYPE_ANSIDATE:
               if value is not None:
                  value = value.isoformat()

         self.domain.__dict__[fld] = value

         self.domain.db.__dict__['rownum'] = self.rownum
      
      if self.domain.isOk:
         self.domain.isOk = self.domain.afterRead()
      else:
         self.domain.afterRead()

      return self.domain


class SqlConverter(object):
   """
   Behandlung von Domainfeldnamen
   bei where und orderby Optionen.

   Reagiert auf die Konfigurationsvariable
   SqlConverter_fieldBegin und SqlConverter_fieldEnd
   sind beide auf None gesetzt, wird keine Umwandlung durchgefuehrt.

   Sucht das Vorkommen von [fieldBegin]domainfeldname[fieldEnd] und ersetzt
   dieses durch den Tabellenfeldnamen

   Beispiel:
      fieldBegin = '$'
      fieldEnd   = ''

      aus Domain fields Definition:
         'personID':{dbfield:'PERSON_ID', ...}

      Ergebnis:
         "$personID = 23" wird zu "PERSON_ID = 23"

   """

   def convert(domain,klausel):
      """
      Konvertierroutine,
      kann als Klassenmethode aufgerufen werden.

      @param   domain         Domainobjekt
      @param   klausel        Zu konvertierende Klausel

      @return  veraenderte Whereklausel

      """

      config = Config()
      fieldBegin = config.SqlConverter_fieldBegin
      fieldEnd   = config.SqlConverter_fieldEnd

      # Ist Beginn und Ende Kennung None,
      # ist die Umwandlung ausgeschalten
      #
      if fieldBegin is None and fieldEnd == None: return klausel
      # Ist Uebersetzung notwendig?
      try:
         klausel.index(fieldBegin)
      except: return klausel

      fieldlist = []

      for fld in domain.meta['fields']:
         fieldlist.append([fld,domain.meta['fields'][fld]['dbfield']])


      for conv in fieldlist:
         repl = fieldBegin+conv[0]+fieldEnd
         klausel = klausel.replace(repl,conv[1])

      return klausel

   convert = staticmethod(convert)

   def handleFilterOption(domain=None,filter=None,dbtype=None):
      """
      Behandelt die Filteroption
      Deatilierte Beschreibung in der Domain Klasse

         HINT:
            Liefet ein Tuple zurueck
            1. Element eine Whereklausel
            2. Element Einen Datenstruktur.
                       Diese ist abhaengig vom Datenbanktyp
                       Oracle ist ein Dictionary
                       alle anderen eine Liste mit dem Filterwert(value)
      @param      domain            Domainobjekt
      @param      filter            Filteroption (String oder Dictionary)
      @param      dbtype            Datenbanktpy

      @return     tuple mit Ergenissen

      """
      included = domain.getDbFieldNames()
      if dbtype is None:
         dbtype = domain.db.dbtype

      value = None
      include = None
      exclude = None
      useLike = False

      if  isinstance(filter,dict) :
         # Option value
         if not 'value' in filter:
            value = ''
         else:
            value = filter['value']

         # Nur spezielle Felder
         if 'include' in filter:
            if isinstance(filter['include'],str):
               filter['include'] = [filter['include']]
            if not '*' in filter['include']:
               included = []
               for fld in filter['include']:
                  included.append(SqlConverter.convert(domain,fld))

         # Auszuschliessende Felder
         if 'exclude' in filter:
            if isinstance(filter['exclude'],str):
               filter['exclude'] = [filter['exclude']]
            for fld in filter['exclude']:
               fld = SqlConverter.convert(domain,fld)
               try:
                  included.remove(fld)
               except:
                  raise Exception('Feld {0} nicht in Domain gefunden'.format(fld))
      else:
         value = filter

      if value.find('%') != -1 or value.find('_') != -1:
         useLike = True

      auxWhere    = []
      auxValues   = []

      for fld in included:
         if dbtype == domain.db.DBTYPE_ORACLE:
            if useLike:
               auxWhere.append('{0} like :filter'.format(fld))
            else:
               auxWhere.append('{0}=:filter'.format(fld))
         elif dbtype == domain.db.DBTYPE_MYSQL:
            if useLike:
               auxWhere.append('{0} like %s'.format(fld))
            else:
               auxWhere.append('{0}=%s'.format(fld))
         else:
            if useLike:
               auxWhere.append('{0} like ?'.format(fld))
            else:
               auxWhere.append('{0}=?'.format(fld))
         auxValues.append(value)

      if dbtype == domain.db.DBTYPE_ORACLE:
         auxValues = {'filter':value}

      retval = ' OR '.join(auxWhere),auxValues

      return (retval)

   handleFilterOption = staticmethod(handleFilterOption)

   def setSelectAndValue(domain,where=None,filter=None,orderby=None,listoption='*'):
      """
      Analysiert where und Filter Option und setzt in der Domain
      die Sqlklausel und ggf. die Werteliste.

      @param   domain         Domain
      @param   where          Where Klausel
      @param   filter         Filter Option
      @param   orderby        Order By Klausel


      """

      whereText = ''
      orderbyText = ''
      values = []
      domain.lastsqlvalues = []
      domain.lastsql = None

      if orderby is not None :
         orderby = SqlConverter.convert(domain,orderby)
         orderbyText = ' order by '+orderby

      if where is not None :
         where = SqlConverter.convert(domain,where)
         whereText = ' where '+where

      if filter is not None:
         (where,domain.lastsqlvalues) = SqlConverter.handleFilterOption(domain=domain,filter=filter)

         whereText = whereText.replace(' where ',' AND ')
         domain.lastsql = 'select {4} from {0} where ({1}) {2} {3}'.format(domain.meta['tablename'],where,whereText,orderbyText,listoption)

      else:
         #domain.lastsql = 'select * from '+domain.meta['tablename']+whereText+orderbyText
         domain.lastsql = 'select {0} from {1} {2} {3}'.format(listoption,domain.meta['tablename'],whereText,orderbyText)
      domain.lastsql = domain.lastsql.strip(' ')

   setSelectAndValue = staticmethod(setSelectAndValue)

