$(function () {
    window.tanda = window.tanda || {};
    window.tanda.autocomplete = window.tanda.autocomplete ||
        {
            config: {
                autocompleteUrl: "/autocomplete"
            },
            wire: function (labelId, url) {
                var idSplit = labelId.split("-");
                idSplit.shift();
                var valueId = idSplit.join("-");
                $("#" + labelId).autocomplete({
                    source: function (request, response) {
                        $.ajax({
                            url: window.tanda.autocomplete.config.autocompleteUrl,
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
                        $("#" + labelId).val(ui.item.label);
                        $("#" + valueId).val(ui.item.value);
                        return false;
                    }
                });
            },
            init: function () {
                $(".autocomplete-label").each(function () {
                    var labelId = $(this).attr("id");
                    window.tanda.autocomplete.wire(labelId);
                });
                console.log("autocomplete loaded.");
            }
        }
    window.tanda.autocomplete.init();
});