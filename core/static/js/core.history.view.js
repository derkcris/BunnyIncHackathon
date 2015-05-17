/*
 * Domain: core.history.view
 */

function showModalHandler(event){
	$('.dn-place-id').val( $(event.target).data('place-id') );
	$('.dn-place-name').val( $(event.target).data('place-name') );
	$('.dn-base-price').val( $(event.target).data('place-price') );
	$('.dn-event-price').val( $(event.target).data('place-price') );
	$('.dn-event-days').val( 1 );
	$('#dn-add-place-modal').modal();
}

function updateDaysHandler(event){
	var price_base = $('.dn-base-price').val();
	var days = $('.dn-event-days').val();
	if(days >= 1){
		$('.dn-event-price').val( price_base * days );
	}
}

function beforeSend(){
	$('.dn-form-submit').attr('disabled', 'disabled');
}

function success(data){
	console.log(data); // TODO remove
	if(data['status'] && data['status'] == 'success'){
		$('.dn-form-container').addClass('hide');
		$('.dn-form-submit').addClass('hide');
		$('.dn-success').removeClass('hide');
	} else {
		error();
	}
}

function error(){
	$('.dn-form-submit').removeAttr('disabled');
}

function submitHandler(event){
	console.log('submitHandler'); // TODO remove
	event.preventDefault();
	if($('.dn-event-start').val() == ''){
		return false;
	}
	if($('.dn-event-days').val() == ''){
		return false;
	}

	var data = {
		'csrfmiddlewaretoken'	: $('.dn-form-add-place').find("input[name*='csrfmiddlewaretoken']").val(),
		'place'					: $('.dn-place-id').val(),
		'start'					: $('.dn-event-start').val(),
		'days'					: $('.dn-event-days').val()
	};
	$.ajax({
		url : '/history/ajax_add_place/',
		type : 'post',
		cache : false,
		data : data,
		dataType : "json",
		beforeSend : beforeSend,
		success : success,
		error: error
    });
};

/* Binding */
$('.dn-event-start').datepicker({altFormat:'yyyy-mm-dd'});
$('.dn-book').click(showModalHandler);
$('.dn-event-days').change(updateDaysHandler);
$('.dn-form-submit').click(submitHandler);