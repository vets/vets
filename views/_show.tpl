%rebase('layout.tpl', title=title, nav=nav, message=message)

<table border="0">
%for idx, col in enumerate(cols):
  %if idx % 2:
  <tr class="highlight">
  %else:
  <tr >
  %end
   <td><b>{{col}}<b></td>
   <td>{{row[idx]}}</td>
  </tr>
%end
</table>

%#if admin == True:
%if defined('delete'):
<form method="POST" action="/{{node}}/{{id}}/delete">
<input type="submit" value="Confirm"/>
<a href="/{{node}}/{{id}}"><input type="button" value="Cancel" /></a>
</form>
%else:
<a href="/{{node}}"><input type="button" value="Back" /></a>
<a href="/{{node}}/{{id}}/edit"><input type="button" value="Edit" /></a>
<a href="/{{node}}/{{id}}/delete"><input type="button" value="Delete" /></a>
%end
%#end
