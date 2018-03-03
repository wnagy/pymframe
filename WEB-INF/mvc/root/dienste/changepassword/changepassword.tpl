<h1 class="blockname">Umsetzen Passwort f&uuml;r "<%out(user)%>"</h1>
<p>
Das Passwort muss mindestens 8 Zeilen lang sein. Es muss Gro&szlig;- und Kleinbuchstaben und mindestens eine Zahl oder Sonderzeichen enthalten.
</p>
<%

out(taglib.form())
out(taglib.hidden('path',cgiparam('path')))
out(taglib.table(colgroup='2'))
out(taglib.hidden('action','run'))
%>
<tr><td>Altes Passwort:</td><td><input type="password" name="oldpw" /></td></td>&nbsp;</td></tr>
<tr><td>Neues Passwort:</td><td><input type="password" name="newpw" /></td></td>&nbsp;</td></tr>
<tr><td>Kontrolle:</td><td><input type="password" name="checkpw" /></td></td>&nbsp;</td></tr>
<tr><td colspan="99"><input type="submit" value="Los!" />
<%
out(taglib.endtable())
out(taglib.endform())
%>
