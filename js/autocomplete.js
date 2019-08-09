$(function () {
    window.tanda = window.tanda || {};
    window.tanda.autocomplte = window.tanda.autocomplete ||
        {
            wire: function (elem, url, ) {
                $("#people-address-auto").autocomplete({
                    source: function (request, response) {
                        // Fetch data
                        $.ajax({
                            url: "/autocomplete",
                            type: 'post',
                            dataType: "json",
                            data: {
                                search: request.term
                            },
                            success: function (data) {
                                response(data);
                            }
                        });
                    },
                    select: function (event, ui) {
                        // Set selection
                        $('#people-address-auto').val(ui.item.label); // display the selected text
                        $('#people-address').val(ui.item.value); // save selected id to input
                        return false;
                    }
                });
            },
            init: function () {
                $(".autocomplete-label").each(function () {
                    var autocompleteLabelId = $(this).id();
                    //window.tanda.autocomplete.wire();
                });
            }
        }
    window.tanda.autocomplete.init();
});