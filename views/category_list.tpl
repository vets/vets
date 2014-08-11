%rebase ('layout.tpl', title=title, nav=nav, message=message)

<a href="/categories/new"><input type="button" value="New"/></a>
%if status == 'active':
<a href="/categories/inactive"><input type="button" value="Inactive"/></a>
%else:
<a href="/categories"><input type="button" value="Active"/></a>
%end

<table border="0">
  <th>Name</th>
  <th>Status</th>
  %for idx, row in enumerate(rows):
    %if idx % 2:
      <tr class="highlight">
    %else:
      <tr>
    %end
        <td>{{row['name']}}</td>
        <td>{{row['status']}}</td>
        <td><a href="/categories/{{row['id']}}/edit"><input type="button" value="Edit" /></a></td>
      </tr>
  %end
</table>
