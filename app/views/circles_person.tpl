% rebase('views/base.tpl', title='Circle Participant')

<h2>{{model.circle_name}} - {{model.person_name}}</h2>

<div id="payments" class="managerPane">

    <h2>Payments</h2>
    <div class="tables" id="payments-table">
        % include('views/item_table.tpl', items=items)
    </div>
    
    <div class="inputForm hidden" id="editForm-payments">

        <h2>Payments</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <input class="payments" type="text" id="payments-account" value="{{model.account}}"/>
        <input class="payments" type="text" id="payments-person" value="{{model.personid}}"/>
        <input class="payments" type="text" id="payments-circle" value="{{model.circleid}}"/>

        <label for="payments-date">Date</label>
        <input class="payments" type="date" id="payments-date" />
        <div class="clear"></div>

        <label for="payments-type">Payment Type</label>
        <div class="clear"></div>
        <select class="payments" id="payments-type">
            <option selected value="credit">Payment</option>
            <option value="debit">Payout</option>
        </select><br/>
        <div class="clear"></div>

        <label for="payments-amount">Amount ($)</label>
        <input class="payments" type="number" step="100" id="payments-amount" />
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-payments">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>

</div>

<script>
    $(function(){

        // Search payer by name or enter account number
        $("#searchPayerBy").change(function() {
            var changeVal = $(this).val();
            if (changeVal === "account") {
                $("#payByAccount").removeClass("hidden");
                $("#payments-account").addClass("payments");

                $("#payByPerson").addClass("hidden");
                $("#payments-person").removeClass("payments");
            }
            if (changeVal === "person") {
                $("#payByPerson").removeClass("hidden");
                $("#payments-person").addClass("payments");

                $("#payByAccount").addClass("hidden");
                $("#payments-account").removeClass("payments");
            }
        });

        // Select if payment or credit
        

    });
</script>