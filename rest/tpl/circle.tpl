% rebase('tpl/base.tpl', title='Circle')
<span id="circleId" data-id="{{model.id}}"></span>
<h1>{{model.name}}</h1>


<br/><br/>
<select id="addPersonSelect">
    <option></option>
    % for p in model.people_list:
    <option value="{{p[0]}}">{{p[1]}} {{p[2]}}</option>
    % end
</select>

<button id="addCirclesPeople" type="button">Add</button>

<div id="circles_people" class="managerPane">

    <h2>People</h2>
    <div id="circles_people-table">
        % include('tpl/item_table.tpl', items=items)
    </div>


    <div class="inputForm hidden" id="editForm-circles_people">

        <h2>People</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-circles_people">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>

</div>

<script src="/static/js/tables.js"></script>
<script src="/static/js/circle.js"></script>