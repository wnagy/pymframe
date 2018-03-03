<h1 class="blockname"%>Pesonen Export<h1/>
<%
from domain.lovdomain         import LovDomain
from domain.gruppedomain      import GruppeDomain

lov = LovDomain(controller.db)
gruppe = GruppeDomain(controller.db)


out('<div class="kriterien">&nbsp;')
out('<form name="edit-1"  style="display:inline;" method="post">'+
    ' &nbsp;Filter: ')
out('<input type="hidden" name="path" value="/root/dienste/doabfrage/weitereabfragen/personen" />')
out('<input type="hidden" name="action" value="run" />')
out('<input type="text" name="_filter" value="*" id="_filter"/>')
out(' Art:',taglib.promptinput(
      prompt="&nbsp;Art",
      name='_perArt',
      type='select',
      datasource=lov.getDatasource('PERSONART',orderby='lovFlag1',addempty='*'),
      value=cgiparam('_perArt') or 'MA',
      nvl='',
      tableRowMode=taglib.TABLE_USE_NONE
      )
   )
out(' Status:',taglib.promptinput(
      prompt="&nbsp;Status",
      name='_perStatus',
      type='select',
      datasource=lov.getDatasource('PERSONSTATUS',orderby='lovFlag1',addempty='*'),
      value=cgiparam('_perStatus') or 'ANGEMELDET',
      nvl='',
      tableRowMode=taglib.TABLE_USE_NONE
      )
   )
out(' Gruppe:',
   taglib.promptinput(
      prompt='&nbsp;Gruppe',
      name='_grpID',
      type='select',
      datasource=gruppe.getDatasource(addempty='*'),
      value=cgiparam('_grpID'),
      tableRowMode=taglib.TABLE_USE_NONE
      )
   )
out('<input type="submit" value="Los!">')
out('</form>')
out('</div>')
out('<script type="text/javascript">document.getElementById("_filter").focus();</script>')
%>

<p>
<h2>Exportiert in Excel 95-2000</h2>
</p>