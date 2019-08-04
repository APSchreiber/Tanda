% rebase('tpl/base.tpl', title='Tanda - Places')
<div id="places" class="managerPane">
    <h1>Places</h1>

    <div class="clear"></div>

    <div id="places-table">
        % include('tpl/item_table.tpl', items=items)
    </div>

    <div class="inputForm hidden" id="editForm-places">

        <h2>Places</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <label for="places-address1">Address 1</label>
        <input class="places" type="text" id="places-address1" />
        <div class="clear"></div>

        <label for="places-address2">Address 2</label>
        <input class="places" type="text" id="places-address2" />
        <div class="clear"></div>

        <label for="places-city">City</label>
        <input class="places" type="text" id="places-city" />
        <div class="clear"></div>

        <label for="places-state">State</label>
        <input class="places" type="text" id="places-state" />
        <div class="clear"></div>

        <label for="places-zip">Zip</label>
        <input class="places" type="text" id="places-zip" />
        <div class="clear"></div>

        <label for="places-country">Country</label>
        <input class="places" type="text" id="places-country" />
        <div class="clear"></div>

        <label for="places-description">Description</label>
        <textarea class="places" type="text" id="places-description"></textarea>
        <div class="clear"></div>

        <label for="places-comments">Comments</label>
        <input class="places" type="text" id="places-comments" />
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-places">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>
</div>

<script>
    $(document).ready(function () {
        window.tanda.tables.init();
        window.tanda.tables.displayItems("places");
    })
</script>