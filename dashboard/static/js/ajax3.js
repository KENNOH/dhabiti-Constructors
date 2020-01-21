$(function() {
	// body...
	$('#search').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/executive/search/",
			data: {
				search_text : $('#search').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#search-results').html(data);
}