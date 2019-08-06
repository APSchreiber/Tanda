% rebase('tpl/base.tpl', title='Circle')
<span id="circleId" data-id="{{model.id}}"></span>
<h1>{{model.name}}</h1>

<h2>People</h2>
<ul>
% for p in model.participants:
  <li>{{p[2]}} {{p[3]}}</li>
% end
</ul>

<br/><br/>
<select id="addPersonSelect">
    <option></option>
    % for p in model.people_list:
    <option value="{{p[0]}}">{{p[1]}} {{p[2]}}</option>
    % end
</select>

<button id="addPerson" type="button">Add</button>

<script src="/static/js/circle.js"></script>