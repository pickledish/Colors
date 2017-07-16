$(document).ready(function() 
{
	console.log("hello")

	$(document).on('click', '.response', function(event) {

		var response = event.target.id == "no" ? 0 : 1

		console.log("clicked")

		var color1 = $("#col1").text()
		var color2 = $("#col2").text()
		
		$.ajax({
			url: '/handleResponse',
			type: 'GET',
			dataType: 'json',
			data: {color1: color1, color2: color2, response: response},
			success: function(json) {

				bg1 = json['color1']
				bg2 = json['color2']

				$("#card1").css('background-color', bg1);
				$("#card2").css('background-color', bg2);

				var color1 = $("#col1").text(bg1)
				var color2 = $("#col2").text(bg2)
			}
		})
	});

});