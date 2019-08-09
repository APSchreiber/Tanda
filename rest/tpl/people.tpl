% rebase('tpl/base.tpl', title='Tanda - People')
<div id="people" class="managerPane">
    <h1>People</h1>

    <div class="clear"></div>

    <div id="people-table">
        % include('tpl/item_table.tpl', items=items)
    </div>

    <div class="inputForm hidden" id="editForm-people">

        <h2>People</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <label for="people-eto">ETO#</label>
        <input class="people" type="text" id="people-eto" />
        <div class="clear"></div>

        <label for="people-first">First Name</label>
        <input class="people" type="text" id="people-first" />
        <div class="clear"></div>

        <label for="people-last">Last Name</label>
        <input class="people" type="text" id="people-last" />
        <div class="clear"></div>

        <label for="people-middle">Middle Name</label>
        <input class="people" type="text" id="people-middle" />
        <div class="clear"></div>

        <label for="people-suffix">Suffix</label>
        <input class="people" type="text" id="people-suffix" />
        <div class="clear"></div>

        <label for="people-phone">Phone</label>
        <input class="people" type="text" id="people-phone" />
        <div class="clear"></div>

        <label for="people-email">Email</label>
        <input class="people" type="text" id="people-email" />
        <div class="clear"></div>

        <label for="people-dob">Date of Birth</label>
        <input class="people" type="date" id="people-dob" />
        <div class="clear"></div>

        <label for="people-address">Address</label>
        <input class="people autocomplete-value" type="text" id="people-address" />
        <input type="text" class="autocomplete-label" id="autocomplete-people-address" />
        <div class="clear"></div>

        <label for="people-description">Description</label>
        <textarea class="people" type="text" id="people-description"></textarea>
        <div class="clear"></div>

        <label for="people-comments">Comments</label>
        <textarea class="people" type="text" id="people-comments"></textarea>
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-people">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>
</div>

<script>
    $(document).ready(function () {
        window.tanda.tables.init();
        window.tanda.tables.displayItems("people");
    });
</script>