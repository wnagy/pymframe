<h1 class="blockname">Hilfs und Wartungs Skripte</h1>
<div class="kriterien">
<%
out(taglib.form())
out(taglib.hidden('path',cgiparam('path')))
out(taglib.hidden('action','run'))
out('Skript: <select name="filename">')
for f in files:
   out('<option value="{0}">{0}</option>'.format(f))
out('</select>')
out('<input type="submit" value="Run!" />')
out(taglib.endform())
%>

</div>
