$(document).ready(function(){
    $(".brick").on("mouseenter",function() {
		$(this).find(".brick-app-extinfo").fadeIn(300);
	});
	$(".brick").on("mouseleave",function(){
		$(this).find(".brick-app-extinfo").fadeOut(300);
	});

    if ($('.user-claim-count').text().valueOf() != '0')
    {
        $('.user-claim-count').show();
    };

    $("#selectall").on('change', function(){

        if($(this).is(":checked"))
        {
            $("#app-list tbody td input:checkbox:not(:disabled)").prop("checked", true);
        }
        else
        {
            $("#app-list tbody td input:checkbox:not(:disabled)").prop("checked", false);
        }
    });

});
