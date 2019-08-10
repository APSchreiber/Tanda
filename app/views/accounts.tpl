% rebase('views/_base.tpl', title='Tanda - Accounts')
<div id="accounts" class="managerPane">
    <h1>Accounts</h1>

    <div class="clear"></div>

    <div class="tables" id="accounts-table">
        % include('views/_item_table.tpl', items=items)
    </div>

    <div class="inputForm hidden" id="editForm-accounts">

        <h2>Accounts</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <label for="accounts-comments">Comments</label>
        <textarea class="accounts" type="text" id="accounts-comments"></textarea>
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-accounts">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>
</div>