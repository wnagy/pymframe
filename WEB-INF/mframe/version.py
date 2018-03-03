class Version:
   """
   Updates:
   --------
   0.10  11.02.2011
         Checktype als eingen Klasse gemacht
         Dateconverter entwickelt
         Untitest ausgebaut

   0.20  ORACLE Unterstuezung eingebaut

   0.21  16.05.2012
         Verbesserung in der Taglib

   0.3   18.05.2012
         addEntry um addparam erweitert

   0.4   11.06.2012
         Bugfix im dbaccess und taglib

   0.5   Viewhandler
         Bugfix

   0.6   Aenderung im Menu
         Option display [True | False]
         Im Controller kann dies Umgesetzt werden.
         Siehe Details im menu.py

   0.6.1 Grid Layout
         im Viewhandler

   0.7   Handler im Domain eingebaut

   0.8   Bugfix in dbaccess.core
         0.8.3 + Viewhandler
                 Einbau der Mehode nextDomain um mit
                 Fehler bei der Datenbank umzugehen.
               + database.core
                 Bugfix
         0.8.5 Oracle spezielle Insert
               Oracle spezielle update
   0.9   Release Candidat
         Oracle support verbessert
         + in der eachDomain limit eingebaut
         + bei dbaccess methode get bugfix
         + Paginate in viewhandler
         + Vebesserungen im MySQL Handling
         + Sendfile (experimentell)
         + Bugfix
         + Optimierung bei Viewhandler
         + Anpassung mySQL Datumsformat (dateconverter)
         + + Layouts und minor Bugfixes
                     + Bugfix in viewhandler
         + redirect eingebaut
         + Flash angepasst
         + Kleine Anpassungen
         + Bug bei setContainer entfernt
         + Verzeichnis "mvc" kann global installiert sein.
         + CSS Klassen in TD eingebaut
         + In Menue 'id' und 'titel' eingabaut
                     CSS support in Menueeintraegen verbessert.
         + Autocommit bei mySQL eingebaut
         + Verbesserte Fehlermeldung in der Controller Klasse

         + ORA Date
         + ORA Insert bugfix
                     ORA NLS_LANG eingebaut
         + Taglib Anpassungen auf IE8
                     Bei Dateconverter Kommans und Blanks im Datumsstring erlaubt
         + Json fuer dbAccess
         + Fehler in dateconverter gefixed
                     refactoring: == None -> is None != None -> is not None
         + In dbaccess den Datentyp long eingefuehrt
         + + Verbesserte Anzeige wenn ungueltiger Pfad (path) im Aufruf
                     + Verbesserte Anzeige wenn unberechtigter Controlleraufruf
                     + r/w Rechte (z.B. read:r)
         + In Authen Readonly Kennung (xxx:r) eingebaut (isWriteable)
         + -..  Bugfixes
         + Einbau von Formatierungsmoeglichkeiten bei Menueanzeige
         + Bei Sender.sendfile wurde option delete eingebaut
         + Bug in JSON convert in eachDomain
         + Config wird ueber Main in alle abgeleitete Klassen weitergeleitet
         + In Domain wurde eine Routine zur Umwandlung aller gelesenenr Felder
                     in einen gewuenschten Characterset eingebaut, Beispiel: cvtCharset('utf9','latin1')
         + Javascript Events in Taglib, promptinput
         + + Domain sqlite lastAutoincrement
                     + Viewhander, bei run Option show=False,
                       verhindert die Ausgabe des Ergebnisses
         + Fehler bei menuebase bei @url behoben
         + Translation
                     Einbau der Klasse Translat
                     Diese Klasse ermoeglicht die Uebersetzung aus einer INI Datei
                     Siehe naehre Informationen in der Klasse
         + Bugfix in menubase.py
         + Bei LISTEDIT wurde das Verhalten so geaendert,
                     dass nach dem Aendern wieder die Bearbeitungsmaske angezeigt
                     wird. Dies kann durch das Flag keepEdit = [True|False] beeinflusst werden.
         + Verbesserung des Verhaltens bei keepEdit und EDIT-LAYOUT
                    
         + Anpassungen taglib auf HTML5
         + Fuer xDem Import wurde bei Domain (dbaccess.core) die Umewandlungsroutine
                     fuer als String uebergebene Doamin Variable herausgeloest um 
                     extern verwendet werden zu koennen
                     prepareValue (fld,value)
                        + fld          Feldname
                        + value        Inhalt
                     Wenn Ein Fehler auftritt, wird self.hasErrors gesetzt

                     in mframe xdembase.py erweitert.         
        + in Controller writelog eingefuert.+
                     usage self.writelog('logmessage')
                     Schreibt den Angegebenen Text auf syserr

        + onMouseover von save in speichern geaendert.
                     Verbesserte weitergabe von Type-Fehlermeldung in viewer

        + Bei Datevonverter die Fehlende Konvertierung CCYY-MM-DD MI:SC eingebaut.

        + onWrite wird unmitelbar nach onDelete, onUpdate und onInsert
                     ausgefuehrt.
                     dbaccess -> core Problem behoben wenn Tabelle keine
                     Autoincrement hat bei lastAutoincrement.
        + Menubase:
                     einbau einer Moeglichkeit den Controller Eintrag in 
                     einem Menueentry zu aenderb bzw. zur Laufzeit anzugeben
                     setEntryController
        + Viewhandler
                     Verbesesrte Erkennung fuer Listendarstellung
        + Erweiterung von Sidebox auf mehere Ebenen

        + Verbesserung der Rechte hinsichtlich
                     in Verbindung mit Readonly (recht:r)
        + Bei translate wird bei Multiline die Leerzeilen
                     enthalten mit "." (Punkt) markiert.

        + Verbesserung bei Sender Klasse
                     Anpassung an Win32 Umgebung
        + afterRead event
                     bei Domain.get und eachDomain eingebaut.
                     Wird nach jedem lesen aufgerufen.
        + Ermoeglicht das notieren von negativen Rechten
                     wird in Menue -xxx notiert so wird die 
                     Funktion nicht aufgerufen, wenn der Benutzer das
                     recht xx hat.
        + Direktes Zuweisen von Date Feldern bei ORACLE DB
                     wenn von ANSI in Datetime umgewandelt wurde geloest
        + Bugfix: in taglib style Attribute eingebaut

        + Einfuehrung von pbkdf2 Passwortverschluesselung

        + main.py:
                     Ermoeglicht das Abschalten des Standardmodul cgi.py.
        + Abschalten der Authentifizierung ueber config.py moeglich gemacht
                     useauthen=False

        +       SQLITE3: auf db Ebene Transaktionen 
                              self.db.begin([DEFERED|IMMEDIATE|EXCLUSIVE] | EXCLUSIVE)
                              self.db.commit(), 
                              self.db.rollback()

   """
   VERSION = '0.9.22'