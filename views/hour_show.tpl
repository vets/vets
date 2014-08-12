%rebase('layout.tpl', title=title, nav=nav, message=message)

<table border="0">
  <tr> <td><b>Volunteer<b></td> <td>{{values['volunteer']}}</td> </tr>
  <tr> <td><b>Start<b></td> <td>{{values['strftime(\'%m-%d %H:%M\',start)']}}</td> </tr>
  <tr> <td><b>End<b></td> <td>{{values['strftime(\'%m-%d %H:%M\',end)']}}</td> </tr>
  <tr> <td><b>Category<b></td> <td>{{values['category']}}</td> </tr>
</table>

%if defined('delete'):
  <form method="POST" action="/hours/{{id}}/delete">
    <input type="submit" value="Confirm"/>
    <a href="/report"><input type="button" value="Cancel" /></a>
  </form>
%else:
  <a href="/hours/{{id}}/edit"><input type="button" value="Edit" /></a>
  <a href="/hours/{{id}}/delete"><input type="button" value="Delete" /></a>
  <a href="/hours"><input type="button" value="Back" /></a>
%end
