$(document).ready(function() {

    $('#app-detail').popup({
      transition: 'all 0.3s'
    });

    $('.brick').click(function() {
        $('#app-detail').html($.ajax({url:$(this).attr('appurl'), async:false}).responseText);
        $('#app-detail').popup('show');
    });

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


function app_rate(app_id, score, csrf) {
    post_data = {};
    post_data['app_id'] = app_id;
    post_data['score'] = score;
    post_data['action'] = 'rate';
    post_data['csrfmiddlewaretoken'] = csrf;

    $.post('/apps/' + app_id + '/', post_data,
        function(data){
            $('#app-score').html(data);
        },
        'html');

    event.stopPropagation();
};

function app_claim(app_id, action, csrf) {
    post_data = {};
    post_data['app_id'] = app_id;
    post_data['action'] = action;
    post_data['csrfmiddlewaretoken'] = csrf;

    $.post('/apps/'+app_id+'/', post_data);

    event.stopPropagation();
}

function app_is_author(app_id, csrf) {
    post_data = {};
    post_data['app_id'] = app_id;
    post_data['action'] = 'is_author';
    post_data['csrfmiddlewaretoken'] = csrf;

    $.post('/apps/' + app_id + '/', post_data,
        function(data){
            $('#app-detail').html(data);
        },
        'html');

    event.stopPropagation();
}
