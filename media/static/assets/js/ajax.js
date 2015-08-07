$(function(){
	$('#search').keyup(function(){
	$.ajax({
	typ:"POST",
	url:"/search/"
	data:{
	    'search_text': $('#search').val(),
	    'csrfmiddlewaretoken': $("input[name=csrfmeddlewaretoken]").val()
 	},
	success:searchSuccess,
	datatype:'html'

	});
   });

});


function searchSuccess(data,textStatus,jqXHR){

     $('#search-results').html(data);

}
