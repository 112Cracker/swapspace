// handle user click 'favorite' item button in sell item detail page
function sellDetailAddToFavorites(itemId) {
    $.ajax({
        url: "/favorite-sell",
        dataType: "json",
        type: "POST",
        data: {
            itemId: itemId,
            csrfmiddlewaretoken: getCSRFToken()
        },
        success: function() {
            detail_add_favorites(itemId);
        }
    })
}

// handle user click 'favorite' sell item buttin
function addToSellFavorites(itemId) {
    $.ajax({
        url: "/favorite-sell",
        dataType: "json",
        type: "POST",
        data: {
            itemId: itemId,
            csrfmiddlewaretoken: getCSRFToken()
        },
        success: function() {
            add_favorites(itemId);
        }
    })
}


// handle user click 'favorite' item buttin in item detail page
function detailAddToFavorites(itemId) {
    $.ajax({
        url: "/favorite",
        dataType: "json",
        type: "POST",
        data: {
            itemId: itemId,
            csrfmiddlewaretoken: getCSRFToken()
        },
        success: function() {
            detail_add_favorites(itemId);
        }
    })
}


// update favorite to favoroted status in item detail page
function detail_add_favorites(itemId) {
    document.getElementById("id-rate").removeAttribute("onclick");
    document.getElementById("id-rate").classList.add('fas');
    document.getElementById("id-rate").classList.remove('far');
}


// handle user click 'favorite' item buttin in exchange page
function addToFavorites(itemId) {
    $.ajax({
        url: "/favorite",
        dataType: "json",
        type: "POST",
        data: {
            itemId: itemId,
            csrfmiddlewaretoken: getCSRFToken()
        },
        success: function() {
            add_favorites(itemId);
        }
    })
}


// update favorite to favoroted status
function add_favorites(itemId) {
    // TO DO
    // update exchange page
    var favoritesCountElement = document.getElementById("id-favorites-count-" + itemId);
    var numFavorites = parseInt(favoritesCountElement.innerHTML);
    favoritesCountElement.innerHTML = numFavorites + 1;
}


// handle user click 'send request' button
// itemId is other item id
function getMyItems(itemId) {
    $.ajax({
        url: "/myitems/" + itemId,
        dataType: "json",
        success: function(data) {
            update_send_request(data, itemId);
        }
    })
}


// update send_request selection list
function update_send_request(data, itemId) {
    // TO DO
    $(".dropdown-item").remove();
    let items = JSON.parse(data["items"]);
    $(items).each(function() {
        var id = this.pk;

        var $a = $("<a class='dropdown-item' href=/exchange/request/" + this.pk + "%20" + itemId + ">" + this.fields.name + "</a>");
        // $a.click(function(e) {
        //     console.log("clicked on " + $(this).attr('id'));
        //     e.preventDefault();
        //     $("#dropdown-items").find(".active").removeClass("active");
        //     $(this).addClass("active");
        // });
        $("#dropdown-items").prepend($a);
    });
}


function search() {
    var searchInputElement = $("#search-keyword-input");
    var keywords = searchInputElement.val();

    searchInputElement.val('');

    $.ajax({
        url: '/search/' + keywords,
        dataType: 'json',
        success: function(data) {
            refresh_exchange_items(data);
        }
    });
}


function refresh_exchange_items(data) {
    console.log("Refresh exchange items");
    let items = JSON.parse(data["items"]);
    console.log(items);
    $(".col-6.col-lg-4").remove();

    $(items).each(function() {
      $("#id-exchange-items").append(
          "<div class='col-6 col-lg-4'>" +
              "<figure class='effect-ravi' onclick=\"window.location.href='/exchange/items/" + this.pk + "'\" >" +
                      "<img src=/media/"+ this.fields.image1 +" >" +
                  "<figcaption>" +
                      "<p>" +
                          "<a>" +
                              "<span>" +
                                  "<label>" + this.fields.name + "</label>" +
                                  "<br>" +
                                  "<label class='heart'><i onclick='addToSellFavorites(" + this.pk + ")' class='fas fa-heart'></i><label>&nbsp;</label><label id='id-favorites-count-" + this.pk +"'> " + this.fields.favorites + "</label></label>" +
                                  "<br>" +
                                  "<label class='hourglass'><i class='fas fa-dollar-sign'></i>" + this.fields.price +"</label>" +
                              "</span>" +
                          "</a>" +
                      "</p>" +
                  "</figcaption>" +
              "</figure>" +
          "</div>"

        );
    });
}


// helper
function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}
