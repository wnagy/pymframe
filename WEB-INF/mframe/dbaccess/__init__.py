"""
Modul zur Abfragen und Bearbeitung von Datenbanktabelle.

Autor:      W. Nagy
Startdatum: 16.12.2010
Lizenz:     http://creativecommons.org/licenses/by/2.0/at/

Die Daten eines Datensatzes werden in einer Domain gespeichert.

Die Domain kann dazu verwendet werden, Datensatzspezifische
Funktionen als Methode zu halten. z.B. ORM
Naehere Beschreibung am ende der Datei.

Dieses Modul ist fuer sqlite Datenbanken optimiert.

Es bietet die Grundlegenden Funktionen
- Oeffnen der Datenbank
- lesen eines Datensatzes ueber seinen Primary Key
  oder ein beliebige where Klausel
- Itteration von Datensaetzen (eachDomain)
  Mit der Moeglichkeit einen Filter einzusetzen und das Sortierkriterium anzugeben
- Einfuegen eines Datensatzes (insert)
- Aenderung eines Datensatzes (update)
- SQL Aggregatfunktionen (min, max, avg, sum, count)

Besonderheiten:
   eachDomain
      Angabe von limit
      Die Option limit bei eachDomain limitiert die gelieferten Datensaetze
      Sie kann in zwei unteschiedlichen Methoden angegben werden.
      1 limit=[ganzzahl] 
        z.B.: .eachDomain(limit=3) liefert maximal 3 Datensaetze
      2 limit=([offset,anzahl])   
        z.B.: .eachDomain(limit(9,16) ueberliest die 1. 9 Daensaetze und liefert
              maximal 16 zurueck


"""