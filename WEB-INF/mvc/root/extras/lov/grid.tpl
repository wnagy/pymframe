<h1 class="blockname">List of values</h1>
<p style="margin-top:16px;" />
<div id="infobox">
Die LOV ist eine Tabelle zur Speicherung der Strukturdaten der Anwendung. Sie ist als Key/Value Paar speicher organisiert.
Um die Paar gruppieren zu k&ouml;nnen werden diese zu Klassen zusammengefasst.<br />
&Auml;nderungen in dieser Tabelle, sollten von fachkundigem Person vorgenommen werden!
</div>
<%
#
# View fuer das GRID-Layout
#
# Es werden zwei Methoden deklariert
#
# editmask:
#   Das Aussehen der Eiditiermaske
#
# listrow:
#   Das Aussehen der Datenzeile
#

from viewhandler              import Viewhandler
from domain.lovdomain         import LovDomain

viewhandler = Viewhandler(controller=controller)

lov = LovDomain(controller.db)

# Spalten Ueberschriften
colHeader = ['&nbsp;','ID','Klasse','Schl&uuml;ssel','Wert','Flag1','Flag2','Flag3','Flag4','&nbsp;']
#
# Deklarieren von zusaetzlichen (hidden) Feldern
# in Masken
#
addhidden=[
      ['path',path],
      ['_filter',cgiparam('_filter')],
      ['_class',cgiparam('_class')]
   ]

# ### Definition der Editiermaske
#     Diese wird vom Viewhandler Methode gridrow aufgerufen
#     um eine Editiermaske zu erzeugen
#
def editmask(domain):
   retval = []

   lov = LovDomain(controller.db)

   #
   # Beginne von HTML Zeile
   #
   retval.append('<tr>')

   #
   # Regelt das Verhalten ob hinzufuegen oder aendern Schaltflaeche
   #
   pkValue = domain.getValue(domain.getPK())
   if pkValue == None:  # Neuanlage
      retval.append(taglib.promptinput(type='addbutton'))
   else:
      retval.append(taglib.promptinput(type='savebutton'))

   #
   # Den Primary Key in die Form uebernehmen.
   #
   retval.append(
      taglib.promptinput(
         name=domain.getPK(),                # Liefert den Namen des Primary Keyx
         type='displayandhidden',            # Anzeigen und hidden Feld erzeugen
         value=pkValue,                      # Inhalt des Primary Keys
         nvl='',                             # Wenn None dann Leerfeld erzeugen
         tableRowMode=taglib.TABLE_USE_TD    # kene TR fuer dieses Feld
         )
      )

   retval.append(
      taglib.promptinput(
         name='lovClass',
         type='select',
         datasource=lov.getDatasourceClass(),
         value=cgiparam('_class') if domain.lovClass is None else domain.lovClass,
         tableRowMode=taglib.TABLE_USE_TD
         )
      )
   retval.append(
     taglib.promptinput(
        name='lovKey',
        type='text',
        value=domain.lovKey,
        nvl='',
        tableRowMode=taglib.TABLE_USE_TD
        )
     )

   retval.append(
     taglib.promptinput(
        name='lovValue',
        type='text',
        value=domain.lovValue,
        nvl='',
        size='32',
        tableRowMode=taglib.TABLE_USE_TD
        )
     )

   retval.append(
     taglib.promptinput(
        name='lovFlag1',
        type='text',
        value=domain.lovFlag1,
        nvl='',
        size='8',
        tableRowMode=taglib.TABLE_USE_TD
        )
     )

   retval.append(
     taglib.promptinput(
        name='lovFlag2',
        type='text',
        value=domain.lovFlag2,
        nvl='',
        size='8',
        tableRowMode=taglib.TABLE_USE_TD
        )
     )

   retval.append(
     taglib.promptinput(
        name='lovFlag3',
        type='text',
        value=domain.lovFlag3,
        nvl='',
        size='8',
        tableRowMode=taglib.TABLE_USE_TD
        )
     )

   retval.append(
     taglib.promptinput(
        name='lovFlag4',
        type='text',
        value=domain.lovFlag4,
        nvl='',
        size='8',
        tableRowMode=taglib.TABLE_USE_TD
        )
     )

   #
   # Beenden der HTML Zeile
   #
   retval.append('</tr>')

   return retval

# ### Definition einer Datenzeile
#     Wird vom viewhandler aufgerufen um
#     eine Datenzeile zu erzeugen.
#
def listrow(domain):
   row = []
   pkValue = domain.getValue(domain.getPK())

   #
   # Einfuegen der Schaltflaeche
   #
   row.append(taglib.gridButtons(
      id={'name'    :domain.getPK(),
          'value'   :pkValue
          },
      addhidden=addhidden
         )
      )
   #
   # Ausgeben des Primariy Keys
   #
   row.append(str(pkValue))
   row.append(domain.lovClass)
   row.append(domain.lovKey)
   row.append(taglib.truncate(domain.lovValue,32))
   row.append(taglib.truncate(domain.lovFlag1,8))
   row.append(taglib.truncate(domain.lovFlag2,8))
   row.append(taglib.truncate(domain.lovFlag3,8))
   row.append(taglib.truncate(domain.lovFlag4,8))

   # Zusaetzliche Leerspalte
   row.append(' ')

   return row

# Ausgabe der Filtermaske
out(taglib.form())
out(taglib.hidden('path',cgiparam('path','')))
%>
<div class="kriterien">
Filter: <input type="text" name="_filter" value="<%out(cgiparam('_filter','*'))%>" />
<%out(taglib.promptinput(
   prompt='Klasse: ',
   name='_class',
   type='select',
   datasource=lov.getDatasourceClass(addempty='*'),
   value=cgiparam('_class')
   )
 )
%>
<input type="submit" value="Los!" />
</div>
<%
out(taglib.endform())


# Scroll Bereich definieren
out('<div class="scroll">')

# HTML Tabelle und Tabellenkopfe
out(taglib.table(colgroup=len(colHeader)))
out(taglib.tablehead(colHeader))

#
# Ausgeben der Zeilen
#
out(viewhandler.gridrow(
   editmask=editmask,
   listrow=listrow,
   list=list,
   taglib=taglib,
   addhidden=addhidden
   ))

# HTML Tabellenende
out(taglib.endtable())
%>

</div>
<script type="text/javascript">document.getElementById("input-?ID-FELD-EINTRAGEN?").focus();</script>
