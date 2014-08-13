%rebase('layout.tpl', title=title, nav=nav, message=message)

<table border="0">
  <tr> <td><b>Volunteer<b></td> <td>{{values['volunteer']}}</td> </tr>
  <tr> <td><b>Start<b></td> <td>{{values['strftime(\'%m-%d %H:%M\',start)']}}</td> </tr>
  <tr> <td><b>End<b></td> <td>{{values['strftime(\'%m-%d %H:%M\',end)']}}</td> </tr>
  <tr> <td><b>Activity<b></td> <td>{{values['activity']}}</td> </tr>
</table>

<form method="POST" action="/hours/{{id}}/delete">
  <input type="submit" value="Confirm"/>
  <a href="/hours"><input type="button" value="Cancel" /></a>
</form>
