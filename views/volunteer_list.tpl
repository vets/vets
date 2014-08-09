%rebase ('layout.tpl', title=title, nav=nav, message=message)

<a href="/volunteers/new"><input type="button" value="New"/></a>
%if status == 'active':
<a href="/volunteers/inactive"><input type="button" value="Inactive"/></a>
%else:
<a href="/volunteers"><input type="button" value="Active"/></a>
%end

<table border="0">
  <th>Name</th>
  <th>Orientation</th>
  <th>Status</th>
  %for idx, row in enumerate(rows):
    %if idx % 2:
      <tr class="highlight">
    %else:
      <tr>
    %end
        <td><a href="/volunteers/{{row['id']}}">{{row['name']}}</a></td>
        <td>{{row['date(orientation)']}}</td>
        <td>{{row['status']}}</td>
      </tr>
  %end
</table>
