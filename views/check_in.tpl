%rebase ('layout.tpl', title=title, nav=nav, message=message)

<form method="POST" action="/checkin">
<table border="0">
  <tr>
    <td>
      <select name="volunteer_id">
          <option value="">Select Your Name</option>
          %for val in volunteers:
              <option value={{val["id"]}}>{{val["name"]}}</option>
          %end
      </select>
    </td>
    <td><input type="submit" value="Check In" /></td>
  </tr>
</table>
</form>

<table border="0">
  <th>Checked In</th>
  <th>Name</th>
  %for idx, row in enumerate(rows):
    %if idx % 2:
      <tr class="highlight">
    %else:
      <tr>
    %end
        <td>{{row['strftime(\'%m-%d %H:%M\',start)']}}</td>
        <td>{{row['volunteer']}}</td>
        <td><a href="/checkout/{{row['id']}}"><input type="button" value="Check Out"/></a></td>
      </tr>
  %end
</table>
