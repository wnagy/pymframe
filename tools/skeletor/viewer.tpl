<h1 class="blockname">{0}</h1>
<p style="margin-top:16px;" />
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
viewhandler = Viewhandler(controller=controller)


# Spalten Ueberschriften
colHeader = ['&nbsp;','ID','&nbsp;']
#
# Deklarieren von zusaetzlichen (hidden) Feldern
# in Masken
#
addhidden=[
      ['path',path],
      ['_filter',cgiparam('_filter')],
   ]

# ### Definition der Editiermaske
#     Diese wird vom Viewhandler Methode gridrow aufgerufen
#     um eine Editiermaske zu erzeugen
#
def editmask(domain):
   retval = []

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

   # Ab hier weitere Felder mittels promptinput einfuegen
   #
   # VORLAGE:
   #retval.append(
   #   taglib.promptinput(
   #      name='<domain-field-name>',
   #      type='[text|select|textarea|displayandhidden|chooseyear]',
   #      value=domain.<domain-field-name>,
   #      nvl='',
   #      tableRowMode=taglib.TABLE_USE_TD
   #      )
   #   )
   #

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

   # Zusaetzliche Leerspalte
   row.append(' ')

   return row

# Ausgabe der Filtermaske
out(taglib.getFilter(text='Filter:',path=path,default=cgiparam(name='_filter',nvl='*')))

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