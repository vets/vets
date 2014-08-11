%rebase('layout.tpl', title=title, nav=nav, message=message)

<table border="0">
  <tr> <td><b>Volunteer<b></td> <td>{{values['volunteer_id']}}</td> </tr>
  <tr> <td><b>Start<b></td> <td>{{values['start']}}</td> </tr>
  <tr> <td><b>End<b></td> <td>{{values['end']}}</td> </tr>
  <tr> <td><b>Category<b></td> <td>{{values['category_id']}}</td> </tr>
</table>

%if defined('delete'):
  <form method="POST" action="/hours/{{id}}/delete">
    <input type="submit" value="Confirm"/>
    <a href="/hours/{{id}}"><input type="button" value="Cancel" /></a>
  </form>
%else:
  <a href="/hours/{{id}}/edit"><input type="button" value="Edit" /></a>
  <a href="/hours/{{id}}/delete"><input type="button" value="Delete" /></a>
  <a href="/hours"><input type="button" value="Back" /></a>
%end
