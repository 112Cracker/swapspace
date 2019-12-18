function getAllList(){
  $.ajax({
    url:"/shoppingCart/get-shoplist-json",
    dataType:"json",
    success: function(items) {
      updateQuantity(items);
    }
  });
}

function updateQuantity(items){
  var changes = JSON.parse(items['change']);
  var update_number = changes.length-1;
  var totalbundle = 0;
  for (i=0;i<=update_number;i++) {
    this_change = changes[i];
    document.getElementById('buy_item_'+this_change.pk).textContent = this_change.fields.incart_amount;
    document.getElementById('subtotal_'+this_change.pk).textContent = this_change.fields.totalprice;
    totalbundle += Number(this_change.fields.totalprice);
  }
  document.getElementById('totalbundle').textContent = totalbundle;

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

function displayError(message) {
    $("#error").html(message);
}

function addQuantity(itemID) {
  $.ajax({
    url:"/shoppingCart/addQuantity",
    type: "POST",
    data: { current_buy_item_id: itemID,
            csrfmiddlewaretoken: getCSRFToken()},
    dataType: "json",
    success: function(response) {
      if ('error' in response) {
        displayError(response.error);
      } else {
        updateQuantity(response)
      }
    }
  });
}

function minQuantity(itemID) {
  $.ajax({
    url:"/shoppingCart/minQuantity",
    type: "POST",
    data: { current_buy_item_id: itemID,
            csrfmiddlewaretoken: getCSRFToken()},
    dataType: "json",
    success: function(response) {
      if ('error' in response) {
        displayError(response.error);
      } else {
        updateQuantity(response)
      }
    }
  });
}

window.onload=function(){
  getAllList();
}

window.setInterval(getAllList, 5000);
