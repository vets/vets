%rebase('layout.tpl', title=title, nav=nav, message=message)

<table border="0">
  <tr> <td><b>Name<b></td> <td>{{values['name']}}</td> </tr>
  <tr> <td><b>Orientation<b></td> <td>{{values['date(orientation)']}}</td> </tr>
  <tr> <td><b>Status<b></td> <td>{{values['status']}}</td> </tr>
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
