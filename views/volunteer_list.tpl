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
        <td>{{row['name']}}</td>
        <td>{{row['orientation']}}</td>
        <td>{{row['status']}}</td>
        <td><a href="/volunteers/{{row['id']}}/edit"><input type="button" value="Edit" /></a></td>
      </tr>
  %end
</table>
