%rebase ('layout.tpl', title=title, nav=nav, message=message)

<a href="/{{node}}/new"><input type="button" value="New"/></a>

<table border="0">
%for col in cols[1:]:
<th>{{col}}</th>
%end
%for idx, row in enumerate(rows):
  %if idx % 2:
  <tr class="highlight">
  %else:
  <tr>
%end
   <td>
    <a href="/{{node}}/{{row[0]}}">{{row[1]}}</a>
   </td>
   %for idx,col in enumerate(row[2:]):
   <td>{{col}}</td>
   %end
  </tr>
%end
</table>
