%rebase('layout.tpl', title=title, nav=nav, message=message)

<table border="0">
  <tr> <td><b>Name<b></td> <td>{{values['name']}}</td> </tr>
  <tr> <td><b>Status<b></td> <td>{{values['status']}}</td> </tr>
</table>

%if defined('delete'):
  <form method="POST" action="/categories/{{id}}/delete">
    <input type="submit" value="Confirm"/>
    <a href="/categories/{{id}}"><input type="button" value="Cancel" /></a>
  </form>
%else:
  <a href="/categories/{{id}}/edit"><input type="button" value="Edit" /></a>
  <a href="/categories/{{id}}/delete"><input type="button" value="Delete" /></a>
  <a href="/categories"><input type="button" value="Back" /></a>
%end
