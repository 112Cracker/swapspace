


function tradesearch() {
    var searchInputElement = $("#search-keyword-input");
    var keywords = searchInputElement.val();

    searchInputElement.val('');

    $.ajax({
        url: '/trade/search/' + keywords,
        dataType: 'json',
        success: function(data) {
            refresh_trade_items(data);
        }
    });
}

function refresh_trade_items(data) {
    console.log("Refresh exchange items");
    let items = JSON.parse(data["items"]);
    console.log(items);
    $(".col-6.col-lg-4").remove();

    $(items).each(function() {
        console.log(this.fields.name);
        $("#id-trade-items").append(
            "<div class='col-6 col-lg-4'>" +
                "<figure class='effect-ravi' onclick=\"window.location.href='/trade/items/" + this.pk + "'\" >" +
                        "<img src=/media/"+ this.fields.image1 +" >" +
                    "<figcaption>" +
                        "<p>" +
                            "<a>" +
                                "<span>" +
                                    "<label>" + this.fields.name + "</label>" +
                                    "<br>" +
                                    "<label class='heart'><i onclick='addToSellFavorites(" + this.pk + ")' class='fas fa-heart'></i><label>&nbsp;</label><label id='id-favorites-count-" + this.pk +"'> " + this.fields.favorites + "</label></label>" +
                                    "<br>" +
                                    "<label class='hourglass'><i class='fas fa-hourglass-end'></i>" + this.fields.amount +"</label>" +
                                "</span>" +
                            "</a>" +
                        "</p>" +
                    "</figcaption>" +
                "</figure>" +
            "</div>"

        );
    });
}


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
