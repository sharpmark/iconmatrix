$(document).ready(function() {

    $('#app-thumb').popup({
      transition: 'all 0.15s'
    });

    $('.brick').click(function() {
        $('#app-thumb').html($.ajax({url:$(this).attr('appurl'), async:false}).responseText);
        $('#app-thumb').popup('show');
    });

    $(".brick").on("mouseenter",function() {
		$(this).find(".brick-extinfo").fadeIn(300);
	});
	$(".brick").on("mouseleave",function(){
		$(this).find(".brick-extinfo").fadeOut(300);
	});

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


function app_rate(package, score, csrf) {
    post_data = {};
    post_data['package_name'] = package;
    post_data['score'] = score;
    post_data['action'] = 'rate';
    post_data['csrfmiddlewaretoken'] = csrf;

    $.post('/apps/' + package + '/', post_data,
        function(data){
            $('#app-score').html(data);
        },
        'html');

    event.stopPropagation();
};
