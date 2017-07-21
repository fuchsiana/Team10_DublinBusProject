// Ideas for only passing arguments of input field to Flask obtained from https://stackoverflow.com/questions/7849221/ajax-delay-for-search-on-typing-in-form-field
// Code for populating the dropdown menus for origin and destination stops adapted from https://stackoverflow.com/questions/41268096/getting-flask-to-alter-selected-value-in-html-drop-down

var delayTimer;
var route;

function getRoute() {
	console.log("Functon triggered, getting stops");
	clearTimeout(delayTimer);
	delayTimer = setTimeout(function() {
		var route = $('#route'),
			origin = $('#origin'),
			destination = $('#destination');
		console.log("The route is " + route.val());

		function updateOriginStops() {
			// This will update the origin stop list corresponding to whatever route is typed in
			updateSettings();
		}

		function updateDestinationStops() {
			// This will update the destination stop list corresponding to whatever route is typed in - this may not be necessary in the end - origin and destination will have the same stops so may only need to have one function rather than 2
			updateSettings();
		}
        
		// Make the selections disabled while fetching new data
		origin.attr('disabled', true);
		destination.attr('disabled', true);

		function updateSettings() {
			//route = document.getElementById("route").value;
			var jqxhr = $.getJSON("http://127.0.0.1:5000/routes?route=" + route.val(), null, function(data) {
                
				// Populate the origin stops
				origin.empty();
				$.each(data.originStops, function(originStops, value) {
					origin.append($('<option>', {
						value: value,
						text: value
					}, '</option>'));
				});
                
				// Populate the destination stops
				destination.empty();
				$.each(data.destinationStops, function(destinationStops, value) {
					destination.append($('<option>', {
						value: value,
						text: value
					}, '</option>'));
				});
                
				// Remove disabled selections after they have been populated
				origin.removeAttr('disabled');
				destination.removeAttr('disabled');
			})
		}
        
		// Call functions to update origin and destination stops
		updateOriginStops();
		updateDestinationStops();
	}, 2000);
}