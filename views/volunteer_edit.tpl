%rebase('layout.tpl', title=title, nav=nav)

%if defined('id'):
<form method="POST" action="/volunteers/{{id}}/edit">
%else:
<form method="POST" action="/volunteers/new">
%end

<table border='0'>
  <tr>
    <td>Name</td>
    %if defined('id'):
      <td><input name="name" type="text" value="{{values['name']}}"/></td>
    %else:
      <td><input name="name" type="text" value="" placeholder="Last, First" autofocus/></td>
    %end
  </tr>
  <tr>
    <td>Orientation</td>
    %if defined('id'):
      <td><input type="date" name="orientation" value="{{values['orientation']}}"></td>
    %else:
      <td><input type="date" name="orientation" value="{{today}}"></td>
    %end
  </tr>
  <tr>
    %if (not defined('id')) or (defined('id') and (values['status'] == "active")):
      <td><input type="radio" name="status" value="active" checked="checked">Active</td>
      <td><input type="radio" name="status" value="inactive">Inactive</td>
    %else:
      <td><input type="radio" name="status" value="active">Active</td>
      <td><input type="radio" name="status" value="inactive" checked="checked">Inactive</td>
    %end
  </tr>
  <tr>
    %if defined('id'):
      <td><input type="submit" value="Save" /></td>
    %else:
      <td><input type="submit" value="Create" /></td>
    %end
    <td><a href="/volunteers"><input type="button" value="Cancel"/></a></td>
  <tr>
</table>
</form>
