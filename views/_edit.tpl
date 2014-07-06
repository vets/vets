%rebase('layout.tpl', title=title, nav=nav)

%if defined('id'):
<form method="POST" action="/{{node}}/{{id}}/edit">
%else:
<form method="POST" action="/{{node}}/new">
%end

<table border='0'>
%for idx, col in enumerate(cols):
  <tr>
    <td>{{col}}</td>
    %if defined('id'):
     <td><input name="{{col}}" type="text" value="{{values[idx]}}"/></td>
    %else:
     <td><input name="{{col}}" type="text" /></td>
    %end
  </tr>
%end
  <tr>
    %if defined('id'):
     <td><input type="submit" value="Save" /></td>
     <td><a href="/{{node}}/{{id}}"><input type="button" value="Cancel"/></a></td>
    %else:
     <td><input type="submit" value="Create" /></td>
     <td><a href="/{{node}}"><input type="button" value="Cancel"/></a></td>
    %end
  <tr>
</table>
</form>
