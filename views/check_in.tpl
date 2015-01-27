%rebase ('layout.tpl')

<p>
  <form method="POST" action="/checkin">
    <select name="volunteer_id">
        <option value="">Select Your Name</option>
      %for val in volunteers:
        <option value={{val["id"]}}>{{val["name"]}}</option>
      %end
    </select>
    <input type="submit" value="Check In" />
  </form>
</p>

<table border="0">
  <th>Name</th>
  <th>Checked In</th>
  <th></th>
  %for idx, row in enumerate(rows):
    %if idx % 2:
      <tr class="highlight">
    %else:
      <tr>
    %end
        <td>{{row['volunteer']}}</td>
        <td>{{row['strftime(\'%m/%d/%Y %H:%M\',start)']}}</td>
        <td><a href="/checkout/{{row['id']}}"><input type="button" value="Check Out"/></a></td>
      </tr>
  %end
</table>
