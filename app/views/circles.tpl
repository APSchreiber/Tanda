% rebase('views/base.tpl', title='Tanda - Circles')
<div id="circles" class="managerPane">
    <h1>Circles</h1>

    <div class="clear"></div>

    <div class="tables" id="circles-table">
        % include('views/item_table.tpl', items=items)
    </div>

    <div class="inputForm hidden" id="editForm-circles">

        <h2>Circles</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <label for="circles-name">Name</label>
        <input class="circles" type="text" id="circles-name" />
        <div class="clear"></div>

        <label for="circles-start">Start</label>
        <input class="circles" type="date" id="circles-start" />
        <div class="clear"></div>

        <label for="circles-months">Months</label>
        <input class="circles" type="text" id="circles-months" />
        <div class="clear"></div>

        <label for="circles-loan">Loan</label>
        <input class="circles" type="text" id="circles-loan" />
        <div class="clear"></div>

        <label for="circles-capacity">Capacity</label>
        <input class="circles" type="text" id="circles-capacity" />
        <div class="clear"></div>

        <label for="circles-description">Description</label>
        <textarea class="circles" type="text" id="circles-description"></textarea>
        <div class="clear"></div>

        <label for="circles-comments">Comments</label>
        <input class="circles" type="text" id="circles-comments" />
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-circles">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>
</div>