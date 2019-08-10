% rebase('views/_base.tpl', title='Circle Participant')

<h2>Participant Information</h2>

<div id="payments" class="managerPane">

    <h2>Payments</h2>
    <div class="tables" id="payments-table">
        % include('views/_item_table.tpl', items=items)
    </div>


    <div class="inputForm hidden" id="editForm-payments">

        <h2>Payments</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>
        
        <label for="searchPayerBy">Pay By</label>
        <div class="clear"></div>
        <select id="searchPayerBy">
            <option selected value="person">Person</option>
            <option value="account">Account</option>
        </select>
        <div class="clear"></div>

        <span id="payByPerson">
            <label class="hidden" for="payments-person">Person</label>
            <input class="payments autocomplete-value" type="text" id="payments-person" />
            <input type="text" class="autocomplete-label" data-autocomplete-for="people" id="autocomplete-payments-person" />
            <div class="clear"></div>
        </span>

        <span class="hidden" id="payByAccount">
            <label class="hidden" for="payments-account">Account</label>
            <input type="text" id="payments-account" />
            <div class="clear"></div>
        </span>

        <label for="payments-date">Date</label>
        <input class="payments" type="date" id="payments-date" />
        <div class="clear"></div>

        <label for="searchPayerBy">Payment ($)</label>
        <div class="clear"></div>
        <select id="searchPayerBy">
            <option selected value="payment">Participant Payment</option>
            <option value="credit">Payout</option>
        </select>
        <div class="clear"></div>
        <label class="hidden" for="payments-amount">Amount ($)</label>
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