%rebase('layout.tpl', title=title, nav=nav)

<form method="POST" action="/checkout/{{id}}">

<table border='0'>
  <tr>
    <td>Checked In</td> 
    <td>
      %timeval = start
      <input type="date" name="start_date" value="{{timeval.date()}}">
      <select name="start_hour">
        %for val in range(1,13):
          %if val == timeval.hour % 12:
            <option value={{val}} selected>{{val}}</option>
          %else:
            <option value={{val}}>{{val}}</option>
          %end
        %end
      </select>
      :
      <select name="start_minute">
        %for val in range(0,60):
          %if val == timeval.minute:
            <option value={{val}} selected>{{"{:02d}".format(val)}}</option>
          %else:
            <option value={{val}}>{{"{:02d}".format(val)}}</option>
          %end
        %end
      </select>
      <select name="start_ampm">
        %if timeval.hour / 12 == 0:
          <option value="AM" selected>AM</option>
          <option value="PM">PM</option>
        %else:
          <option value="AM">AM</option>
          <option value="PM" selected>PM</option>
        %end
      </select>    
    </td>
  </tr>
  <tr>
    <td>Checked Out</td>
    <td>
      <input type="date" name="end_date" value="{{now.date()}}">
      <select name="end_hour">
        %for val in range(1,13):
          %if val == now.hour % 12:
            <option value={{val}} selected>{{val}}</option>
          %else:
            <option value={{val}}>{{val}}</option>
          %end
        %end
      </select>
      :
      <select name="end_minute">
        %for val in range(0,60):
          %if val == now.minute:
            <option value={{val}} selected>{{"{:02d}".format(val)}}</option>
          %else:
            <option value={{val}}>{{"{:02d}".format(val)}}</option>
          %end
        %end
      </select>
      <select name="end_ampm">
        %if now.hour / 12 == 0:
          <option value="AM" selected>AM</option>
          <option value="PM">PM</option>
        %else:
          <option value="AM">AM</option>
          <option value="PM" selected>PM</option>
        %end
      </select>
    </td>
  </tr>
  <tr>
    <td>Name</td>
      <td>
        <select name="volunteer_id" disabled>
          <option value={{volunteer["id"]}} selected>{{volunteer["name"]}}</option>
        </select>
      </td>
  </tr>
  <tr>
    <td>Activity</td>
    <td>
      <select name="activity_id">
          <option value="">Please Select</option>
        %for val in activities:
          %if val["id"] == values["activity_id"]:
            <option value={{val["id"]}} selected>{{val["name"]}}</option>
          %else:
            <option value={{val["id"]}}>{{val["name"]}}</option>
          %end
        %end
      </select>
    </td>
  </tr>
  <tr>
    <td><input type="submit" value="Check Out" /></td>
    <td><a href="/"><input type="button" value="Cancel"/></a></td>
  <tr>
</table>
</form>
