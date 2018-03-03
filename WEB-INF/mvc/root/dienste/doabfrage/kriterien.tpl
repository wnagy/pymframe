<h1 class="blockname">Abfragen</h1>
<div class="kriterien">
<%
taglib.isReadonly=False
out(taglib.form())
out(taglib.hidden('path',cgiparam('path')))
out(taglib.hidden('action','start'))

out(
   taglib.promptinput(
     name='_abfID',
     prompt='Abfrage:&nbsp;',
     type='select',
     datasource=abfrage.getDatasource(userRights)
     )
   )
out(
   taglib.promptinput(
     name='mode',
     prompt='Ausgabeart:&nbsp;',
     type='select',
     datasource=[
        ['screen','Bildschirm'],
        ['xls','Excel']
        ]
     )
   )
out('<input type="submit" value="Los!" />')
out(taglib.endform())
%>
</div>