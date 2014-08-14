%rebase ('layout.tpl')

<p>
  <a href="/activities/new"><input type="button" value="New"/></a>
  %if status == 'active':
  <a href="/activities/inactive"><input type="button" value="Inactive"/></a>
  %else:
  <a href="/activities"><input type="button" value="Active"/></a>
  %end
</p>

<table border="0">
  <th>Name</th>
  <th>Status</th>
  <th></th>
  %for idx, row in enumerate(rows):
    %if idx % 2:
      <tr class="highlight">
    %else:
      <tr>
    %end
        <td>{{row['name']}}</td>
        <td>{{row['status']}}</td>
        <td><a href="/activities/{{row['id']}}/edit"><input type="button" value="Edit" /></a></td>
      </tr>
  %end
</table>
