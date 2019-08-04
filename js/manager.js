$(document).ready(function(){
	
	var config = tandaConfig;
	
  // Data Tables config
  var dtConfig = {
    buttons: [
      {
        text: "Add",
        action: function ( e, dt, node, config ) {
          addEditItem(node);
        }
      },
      {
        text: "Edit",
        action: function ( e, dt, node, config ) {
          var ids = getSelectedIds(dt);
          if (ids.length == 0 || ids.length > 1) {
            alert("Please select a single row to edit.");
            return;
          }
          addEditItem(node, ids[0]);
        }
      },
      {
        text: "Delete",
        action: function ( e, dt, node, config ) {
          var ids = getSelectedIds(dt);
          if (ids.length == 0 || ids.length > 1) {
            alert("Please select a single row to delete.");
            return;
          }
          if (confirm("Are you sure you want to delete this item?")) {
            deleteItem(node, ids[0]);
          }
        }
      },
      {
        text: "Details",
        action: function ( e, dt, node, config ) {
          var ids = getSelectedIds(dt);
          if (ids.length == 0 || ids.length > 1) {
            alert("Please select a single row to edit.");
            return;
          }
          goToDetails(node, ids[0]);
        }
      }
    ]
  };
  
	/********** Functions **********/
	
  function getDropdown(category, field, t, f) {
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
  }
  
	function getItems(cls) {
		var items = {};
		$("." + cls).each(function(){
			var itemName = $(this).attr("id").split("-")[1];
			var itemVal = $(this).val();
			items[itemName] = itemVal;
		});
		return items;
	}
  
  function setItems(cls, data) {
    for (var key in data) {
      var item = data[key];
      $("#" + cls + "-" + key).val(item);
    }
  }
	
	function postForm(route, formClass, success) {
		var data = getItems(formClass);
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
	}
  
  function closeForms() {
    $(".overlay").addClass("hidden");
    $(".inputForm").addClass("hidden");
    $(".inputForm").find("input, textarea").val("");
    
    $(".inputForm" + " select").each(function() {
      var domainInfo = $(this).attr("data-domain");  
      if (domainInfo) {
        $(this).empty();
      }
    });
    
  }
  
  function getSelectedIds(dt, dataname) {
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
  }
  
  // /********** Top Nav **********/
  // $(".topnav a").click(function() {
  //   var tab = $(this).html();
    
  //   // handle nav highlighting
  //   $(".topnav a").removeClass("active");
  //   $(this).addClass("active");
    
  //   // handle div showing
  //   $(".managerPane").addClass("hidden");
  //   $("#" + tab).removeClass("hidden");
    
  //   displayItems(tab);
    
  // });
  
  /********** Forms control **********/

  function deleteItem(node, id) {
    var category = $(node).closest(".managerPane").attr("id");
    $.ajax({
      type: "GET",
      url: "/r_" + category + "/" + id,
      success: function (r) {
        displayItems(category);
        closeForms();
      }
    });
  }

  function goToDetails(node, id) {
    window.location.href("/circle/1");
  }
  
  function addEditItem(node, id) {
    var category = $(node).closest(".managerPane").attr("id");
    
    // show the form
    $(".overlay").removeClass("hidden");
    $(".inputForm").addClass("hidden");
    $("#editForm-" + category).removeClass("hidden");
    
    // populate the domains TODO fix async bug when editing existing item
    $("#editForm-" + category + " select").each(function() {
      var domainInfo = $(this).attr("data-domain");
      if (domainInfo) {
        var domainInfoSplit = domainInfo.split("-");
        var domainT = domainInfoSplit[0];
        var domainF = domainInfoSplit[1];
        var idInfo = $(this).attr("id").split("-");
        var field = idInfo[1];
        
        getDropdown(category, field, domainT, domainF);
        
      }
      
    });
    
    $(".submitButton").unbind();
    
    // add item
    if (!id) {
      $(".submitButton").bind("click", function() {
      
        var items = getItems(category);
      
        $.ajax({
          type: "POST",
          contentType: "application/json",
          dataType: "json",
          url: "/add_" + category,
          data: JSON.stringify(items),
          success: function (r) {
            displayItems(category);
            closeForms();
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
            setItems(category, r.items[0]);
            
            // set up form submit
            $(".submitButton").bind("click", function() {
            
              var items = getItems(category);
            
              $.ajax({
                type: "POST",
                contentType: "application/json",
                dataType: "json",
                url: "/" + category + "/" + id,
                data: JSON.stringify(items),
                success: function (r) {
                  displayItems(category);
                  closeForms();
                }
              });
            });
            
          }
        });
    }
    
  }
  
  $(".addItemLink").click(function() {
    var category = $(this).attr("id").split("-")[1];
    
    // show the overlay
    $(".overlay").removeClass("hidden");
    
    // show the form
    $(".inputForm").addClass("hidden");
    $("#editForm-" + category).removeClass("hidden");
    
  });
  
	/********** Init **********/
	
	// Init
	// displayItems("people");
	
	/********** Events form **********/
  
	// Get venues for dropdown
	// $.ajax({
		// type: "GET",
		// url: "/venues/json",
		// success: function (r) {
			// console.log(r);
			// for (var i = 0; i < r.items.length; i++) {
				// var venue = r.items[i];
				// var option = '<option value="' + venue.id + '">' + venue.name + '</option>';
				// $("#event-venue").append(option);
			// }
		// }
	// });
	
	// Display Items
	function displayItems(category) {
		$.ajax({
			type: "GET",
			url: "/list_" + category + "/table",
			success: function (r) {
				$("#" + category + "-table").html(r);
        
        $('.data-table').DataTable({
          select: true,
          buttons: dtConfig.buttons,
          dom: "lfrtBip",
          destroy: true,
        });
        
			}
		});
	}
  
  $(".inputForm .closeX").click(function() {
    closeForms();
  });
	
	/********** Defaults for forms from config **********/
	
	// Set up states
	var states = config.geo.states;
	for (var i = 0; i < states.length; i++) {
		var state = states[i];
		var option;
		if (state === config.geo.defaultState) {
			option = '<option selected value="' + state + '">' + state + '</option>';
		}
		else {
			option = '<option value="' + state + '">' + state + '</option>';
		}
		$("#venue-state").append(option);
	}
	
	// Set up country
	if (config.geo.defaultCountry) {
		$("#venue-country").val(config.geo.defaultCountry)
	}
	
});

  