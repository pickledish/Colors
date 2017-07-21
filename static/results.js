$(document).ready(function() 
{
	console.log("Connected");
	var currentPair = 0

	toShow = "#Picture" + (currentPair + 1)
	$(toShow).show()

	$(document).on('click', '.nav', function(event) {

		if (event.target.id == "prev") {
			if (currentPair != 0) {
				changePicture(currentPair - 1)
				currentPair -= 1
			}
		}

		if (event.target.id == "next") {
			if (currentPair != 2) {
				changePicture(currentPair + 1)
				currentPair += 1
			}
		}
		
	});

});

function changePicture(num) {
	
	index = num + 1
	id = "Picture" + index

	$( ".pic" ).each(function( index ) {
		if ($(this).attr('id') == id) {
			$(this).show()
		} else {
			$(this).hide()
		}
	});

}