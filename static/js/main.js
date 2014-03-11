$(document).ready(function(){
    $(".brick").on("mouseenter",function() {
		$(this).find(".brick-app-extinfo").fadeIn(300);
	});
	$(".brick").on("mouseleave",function(){
		$(this).find(".brick-app-extinfo").fadeOut(300);
	});
});
