<div id="menu">
<ul>
  %for v in nav:
    <li><a href='/{{v.lower().replace(' ','')}}'>{{v}}</a></li>
  %end
</ul>
</div>
