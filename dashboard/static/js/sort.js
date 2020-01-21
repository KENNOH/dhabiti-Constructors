$smschange(id){
		$.ajax({
			type: "POST",
            url: "/sort/",
			data: {
                search_text: $('#sort').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#sort-results').html(data);
}

