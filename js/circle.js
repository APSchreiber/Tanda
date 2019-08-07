$(function () {
    window.tanda = window.tanda || {};
    window.tanda.circle = window.tanda.circle ||
    {
        init: function() {
            $("#addCirclesPeople").click(function(){
                var circleId = $("#circleId").data("id");
                var personId = $("#addPersonSelect").val();
                $.ajax({
                    type: "GET",
                    url: "/circles/addperson/" + circleId + "/" + personId,
                    success: function (r) {
                        // for (var i = 0; i < r.items.length; i++) {
                        //     var item = r.items[i];
                        //     var option = '<option value="' + item.id + '">' + item.val + '</option>';
                        //     $("#" + category + "-" + field).append(option);
                        // }
                    }
                });
            });

            $('.data-table').DataTable({
                select: true,
                buttons: window.tanda.tables.dtConfig.buttons,
                dom: "lfrtBip",
                destroy: true,
            });
        }
    }
    window.tanda.circle.init()
});