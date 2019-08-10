% rebase('views/base.tpl', title='Circle Participant')

<h2>Participant Information</h2>

<div id="payments" class="managerPane">

    <h2>Payments</h2>
    <div class="tables" id="payments-table">
        % include('views/item_table.tpl', items=items)
    </div>


    <div class="inputForm hidden" id="editForm-payments"">

        <h2>Payments</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <label for="payments-date">Date</label>
        <input class="payments" type="date" id="payments-date" />
        <div class="clear"></div>

        <label for="payments-amount">Amount</label>
        <input class="payments" type="text" id="payments-amount" />
        <div class="clear"></div>

        <label for="payments-person">Person</label>
        <input class="payments" type="text" id="payments-person" />
        <div class="clear"></div>

        <label for="payments-account">Account</label>
        <input class="payments" type="text" id="payments-account" />
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-payments">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>

</div>