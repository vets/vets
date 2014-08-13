%rebase ('layout.tpl', title=title, nav=nav, message=message)

<form method="POST" action="/hours">
  <table><tr>
    <td>From <input type="date" name="start" value="{{start}}"></td>
    <td>To <input type="date" name="end" value="{{end}}"></td>
    <td>Sum <select name="group_by">
      <option value="">None</option>
      %if group_by == 'volunteer':
        <option value="volunteer" selected>Volunteer</option>
      %else:
        <option value="volunteer">Volunteer</option>
      %end
      %if group_by == 'activity':
        <option value="activity" selected>Activity</option>
      %else:
        <option value="activity">Activity</option>
      %end
    </select></td>
    <td><input type="submit" value="Report" /></td>
    <td><a href="/hours"><input type="button" value="Clear"/></a></td>
  </tr></table>
</form>

%if group_by == '':
<table border="0">
  <th>Checked In</th>
  <th>Checked Out</th>
  <th>Hours</th>
  <th>Name</th>
  <th>Activity</th>
  %for idx, row in enumerate(rows):
    %if idx % 2:
      <tr class="highlight">
    %else:
      <tr>
    %end
        <td>{{row['strftime(\'%m-%d %H:%M\',start)']}}</td>
        <td>{{row['strftime(\'%m-%d %H:%M\',end)']}}</td>
        <td>{{row['totalHours']}}</td>
        <td>{{row['volunteer']}}</td>
        <td>{{row['activity']}}</td>
        <td><a href="/checkout/{{row['id']}}"><input type="button" value="Edit"/></a></td>
        <td><a href="/hours/{{row['id']}}/delete"><input type="button" value="Delete"/></a></td>
      </tr>
  %end
</table>
%else:
<table border="0">
  <th>Name</th>
  <th>Hours</th>
  %for idx, row in enumerate(rows):
    %if idx % 2:
      <tr class="highlight">
    %else:
      <tr>
    %end
      %if group_by == 'volunteer':
        <td>{{row['volunteer']}}</td>
      %elif group_by == 'activity':
        <td>{{row['activity']}}</td>
      %end      
        <td>{{row['totalHours']}}</td>
      </tr>
  %end
</table>
%end
