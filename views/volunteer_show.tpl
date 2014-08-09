%rebase('layout.tpl', title=title, nav=nav, message=message)

<table border="0">
  <tr> <td><b>Name<b></td> <td>{{values[1]}}</td> </tr>
  <tr> <td><b>Orientation<b></td> <td>{{values[2]}}</td> </tr>
  <tr> <td><b>Status<b></td> <td>{{values[3]}}</td> </tr>
</table>

%if defined('delete'):
  <form method="POST" action="/volunteers/{{id}}/delete">
    <input type="submit" value="Confirm"/>
    <a href="/volunteers/{{id}}"><input type="button" value="Cancel" /></a>
  </form>
%else:
  <a href="/volunteers/{{id}}/edit"><input type="button" value="Edit" /></a>
  <a href="/volunteers/{{id}}/delete"><input type="button" value="Delete" /></a>
  <a href="/volunteers"><input type="button" value="Back" /></a>
%end
