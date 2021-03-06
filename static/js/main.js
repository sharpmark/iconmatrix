$(document).ready(function() {

    $('#icon-detail').popup({
      transition: 'all 0.3s'
    });

    $('.brick-small').click(function() {
        $('#icon-detail').html($.ajax({url:'/icons/'+$(this).attr('sid')+'/', async:false}).responseText);

        $('#icon-detail').popup('show');
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

$('#add_more').click(function() {

    selector = '.form-group:last';
    var newElement = $(selector).clone(true);
    var total = $('#id_form-TOTAL_FORMS').val();

    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });

    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });

    $('#id_form-TOTAL_FORMS').val(total + 1);

    $(selector).after(newElement);
});

function rate(icon_id, score, csrf) {

    post_data = {};
    post_data['icon_id'] = icon_id;
    post_data['score'] = score;
    post_data['csrfmiddlewaretoken'] = csrf;

    $.post('/icons/' + icon_id + '/rate/' + score + '/', post_data,
        function(data){
            $('#icon-score').html(data);
        },
        'html');

    event.stopPropagation();
};
