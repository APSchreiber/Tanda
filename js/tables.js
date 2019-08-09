$(function () {
    window.tanda = window.tanda || {};
    window.tanda.tables = window.tanda.tables ||
        {
            config: tandaConfig,

            // Data Tables config
            dtConfig: {
                buttons: [
                    {
                        text: "Add",
                        action: function (e, dt, node, config) {
                            window.tanda.tables.addEditItem(node);
                        }
                    },
                    {
                        text: "Edit",
                        action: function (e, dt, node, config) {
                            var ids = window.tanda.tables.getSelectedIds(dt);
                            if (ids.length == 0 || ids.length > 1) {
                                alert("Please select a single row to edit.");
                                return;
                            }
                            window.tanda.tables.addEditItem(node, ids[0]);
                        }
                    },
                    {
                        text: "Delete",
                        action: function (e, dt, node, config) {
                            var ids = window.tanda.tables.getSelectedIds(dt);
                            if (ids.length == 0 || ids.length > 1) {
                                alert("Please select a single row to delete.");
                                return;
                            }
                            if (confirm("Are you sure you want to delete this item?")) {
                                window.tanda.tables.deleteItem(node, ids[0]);
                            }
                        }
                    },
                    {
                        text: "Details",
                        action: function (e, dt, node, config) {
                            var ids = window.tanda.tables.getSelectedIds(dt);
                            if (ids.length == 0 || ids.length > 1) {
                                alert("Please select a single row to edit.");
                                return;
                            }
                            window.tanda.tables.goToDetails(node, ids[0]);
                        }
                    }
                ]
            },
            getDropdown: function (category, field, t, f) {
                $.ajax({
                    type: "GET",
                    url: "/domains/" + t + "/" + f,
                    success: function (r) {
                        for (var i = 0; i < r.items.length; i++) {
                            var item = r.items[i];
                            var option = '<option value="' + item.id + '">' + item.val + '</option>';
                            $("#" + category + "-" + field).append(option);
                        }
                    }
                });
            },
            getItems: function (cls) {
                var items = {};
                $("." + cls).each(function () {
                    var itemName = $(this).attr("id").split("-")[1];
                    var itemVal = $(this).val();
                    items[itemName] = itemVal;
                });
                return items;
            },
            setItems: function (cls, data) {
                for (var key in data) {
                    var item = data[key];
                    $("#" + cls + "-" + key).val(item);
                }
            },
            postForm: function (route, formClass, success) {
                var data = window.tanda.tables.getItems(formClass);
                $.ajax({
                    type: "POST",
                    contentType: "application/json",
                    dataType: "json",
                    url: "/" + route,
                    data: JSON.stringify(data),
                    success: function (r) {
                        success;
                    }
                });
            },
            closeForms: function () {
                $(".overlay").addClass("hidden");
                $(".inputForm").addClass("hidden");
                $(".inputForm").find("input, textarea").val("");

                $(".inputForm" + " select").each(function () {
                    var domainInfo = $(this).attr("data-domain");
                    if (domainInfo) {
                        $(this).empty();
                    }
                });
            },
            getSelectedIds: function (dt, dataname) {
                var selected = dt.rows({ selected: true });
                var jq = selected.nodes().to$();
                var ids = [];
                dataname = dataname || "id";
                jq.each(function () {
                    var row = $(this);
                    var id = row.data(dataname);
                    if (id != undefined) {
                        ids.push(id);
                        return true;
                    }
                    // fallback
                    dataname = "id";
                    id = $(this).data(dataname);
                    if (id == undefined)
                        return false;
                    ids.push(id);
                });
                if (ids.length > 0)
                    return ids;

                data = selected.data();
                for (var i = 0; i < data.length; ++i) {
                    ids.push(data[i][0]);
                }
                return ids;
            },
            deleteItem: function (node, id) {
                var category = $(node).closest(".managerPane").attr("id");
                $.ajax({
                    type: "GET",
                    url: "/" + category + "/r/" + id,
                    success: function (r) {
                        window.tanda.tables.displayItems(category);
                        window.tanda.tables.closeForms();
                    }
                });
            },

            goToDetails: function (node, id) {
                var category = $(node).closest(".managerPane").attr("id");
                window.location = "/" + category + "/details/" + id
            },

            addEditItem: function (node, id) {
                var category = $(node).closest(".managerPane").attr("id");

                //alert(category);

                // show the form
                $(".overlay").removeClass("hidden");
                $(".inputForm").addClass("hidden");
                $("#editForm-" + category).removeClass("hidden");

                // populate the domains TODO fix async bug when editing existing item
                $("#editForm-" + category + " select").each(function () {
                    var domainInfo = $(this).attr("data-domain");
                    if (domainInfo) {
                        var domainInfoSplit = domainInfo.split("-");
                        var domainT = domainInfoSplit[0];
                        var domainF = domainInfoSplit[1];
                        var idInfo = $(this).attr("id").split("-");
                        var field = idInfo[1];

                        window.tanda.tables.getDropdown(category, field, domainT, domainF);

                    }

                });

                $(".submitButton").unbind();

                // add item
                if (!id) {
                    $(".submitButton").bind("click", function () {

                        var items = window.tanda.tables.getItems(category);

                        // check for additional route params
                        addParams = "";
                        if ($("#editForm-" + category).data("add-route-params")) {
                            var params = $("#editForm-" + category).data("add-route-params");
                            routeParams = [];
                            paramsList = params.split(",");
                            for (var i = 0; i < paramsList.length; i++) {
                                param = paramsList[i];
                                // get param by dom id or other stuff
                                var paramKey = param.split("~");
                                if (paramKey.length > 1) {
                                    // get by dom id
                                    if (paramKey[0] === "dom") {
                                        var getId = paramKey[1];
                                        var getType = paramKey[2];
                                        if (getType === "val") {
                                            param = $("#" + getId).val();
                                        }
                                    }
                                }
                                routeParams.push(param);
                            }
                            for (var i = 0; i < routeParams.length; i++) {
                                addParams += "/" + routeParams[i];
                            }
                        }

                        $.ajax({
                            type: "POST",
                            contentType: "application/json",
                            dataType: "json",
                            url: "/" + category + "/add" + addParams,
                            data: JSON.stringify(items),
                            success: function (r) {
                                window.tanda.tables.displayItems(category);
                                window.tanda.tables.closeForms();
                            }
                        });
                    });
                }
                // edit item
                else {
                    // get item data
                    $.ajax({
                        type: "GET",
                        contentType: "application/json",
                        dataType: "json",
                        url: "/" + category + "/" + id,
                        success: function (r) {
                            // populate form
                            console.log("Item Back:");
                            console.log(r);
                            window.tanda.tables.setItems(category, r.items[0]);

                            // set up form submit
                            $(".submitButton").bind("click", function () {

                                var items = window.tanda.tables.getItems(category);

                                $.ajax({
                                    type: "POST",
                                    contentType: "application/json",
                                    dataType: "json",
                                    url: "/" + category + "/" + id,
                                    data: JSON.stringify(items),
                                    success: function (r) {
                                        window.tanda.tables.displayItems(category);
                                        window.tanda.tables.closeForms();
                                    }
                                });
                            });

                        }
                    });
                }
            },
            displayItems: function (category) {
                $.ajax({
                    type: "GET",
                    url: "/" + category + "/list/table",
                    success: function (r) {
                        $("#" + category + "-table").html(r);

                        $('.data-table').DataTable({
                            select: true,
                            buttons: window.tanda.tables.dtConfig.buttons,
                            dom: "lfrtBip",
                            destroy: true,
                        });

                    }
                });
            },
            init: function () {

                $(".addItemLink").click(function () {
                    var category = $(this).attr("id").split("-")[1];

                    // show the overlay
                    $(".overlay").removeClass("hidden");

                    // show the form
                    $(".inputForm").addClass("hidden");
                    $("#editForm-" + category).removeClass("hidden");

                });

                $(".inputForm .closeX").click(function () {
                    window.tanda.tables.closeForms();
                });

                var states = window.tanda.tables.config.geo.states;
                for (var i = 0; i < states.length; i++) {
                    var state = states[i];
                    var option;
                    if (state === window.tanda.tables.config.geo.defaultState) {
                        option = '<option selected value="' + state + '">' + state + '</option>';
                    }
                    else {
                        option = '<option value="' + state + '">' + state + '</option>';
                    }
                    $("#venue-state").append(option);
                }

                // Set up country
                if (window.tanda.tables.config.geo.defaultCountry) {
                    $("#venue-country").val(window.tanda.tables.config.geo.defaultCountry)
                }
            }
        }

});