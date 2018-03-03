<h1 class="blockname">Abfragen <%out(abfrage.abfName)%> (<%out(abfrage.abfID)%>)</h1>
<div class="kriterien">
<%
out(taglib.form(method="get"))
out(taglib.hidden('path',cgiparam('path')))
out(taglib.hidden('mode',cgiparam('mode')))
out(taglib.hidden('action','query'))
out(taglib.hidden('_abfID',str(abfrage.abfID)))

lstNames = list()

out(taglib.table(colgroup=3))
out('<tr><th>Fld</th><th>Wert</th><th>&nbsp;</th></tr>')
for ln in prompts:
   val =ln.replace('-- prompt ','')
   (name,sPrompt) = val.split('=')
   lstNames.append(name)

   if sPrompt.startswith('[['):
      out(
         taglib.promptinput(
            name=name,
            prompt=name,
            type='select',
            datasource=eval(sPrompt),
            value='',
            more=['title="{0}"'.format(name)],
            tableRowMode=taglib.TABLE_USE_TRTD,
            isReadonly=False
         )
      )
   else:
      out(
         taglib.promptinput(
            name=name,
            prompt=sPrompt,
            type='text',
            value='',
            size='128',
            more=['title="{0}"'.format(name)],
            tableRowMode=taglib.TABLE_USE_TRTD,
            isReadonly=False
         )
      )
out(taglib.endtable())

out('<input type="hidden" value="{0}" name="lstPrompts" />'.format(','.join(lstNames)))
out('<input type="submit" value="Los!" />')
out(taglib.endform())
%>

</div>