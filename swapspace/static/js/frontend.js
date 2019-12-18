// $(document).ready(function() {
// 	$(".navbar-nav .nav-item .nav-link").on("click", 
// 	    function(){
// 		    $(".navbar-nav").find(".active").removeClass("active");
// 		    $(this).parent(".nav-item").addClass("active");
// 		    console.log($(this).parent(".nav-item"));
// 	});

// });

$(document).ready(function(){
	$('.navbar-nav .nav-item').click(function(){
	    $('.navbar-nav .nav-item').removeClass('active');
	    $(this).addClass('active');
	})
});