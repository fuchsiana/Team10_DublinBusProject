// Ideas for only passing arguments of input field to Flask obtained from https://stackoverflow.com/questions/7849221/ajax-delay-for-search-on-typing-in-form-field
// Code for populating the dropdown menus for origin and destination stops adapted from https://stackoverflow.com/questions/41268096/getting-flask-to-alter-selected-value-in-html-drop-down
var delayTimer;

function getDirection() {
    // Function to get the directions that the route can go in - then populates the direction dropdown
	console.log("Getting directions...");
	clearTimeout(delayTimer);
	delayTimer = setTimeout(function() {
		var route = $('#route'),
			direction = $('#direction');
		console.log("The route is " + route.val());

		function updateDirection() {
			// This will update the direction list corresponding to whatever route is typed in
			updateDirectionSettings();
		}
		// Make the selections disabled while fetching new data
		direction.attr('disabled', true);

		function updateDirectionSettings() {
			var jqxhr = $.getJSON("http://127.0.0.1:5000/direction?route=" + route.val(), null, function(data) {
				direction.empty();
                
                // Populate the first option in direction with "Select direction" - this will be disabled and won't be able to be selected
				direction.append($('<option>', {
					value: "",
					text: "Select direction"
				}, '</option>'));
				// To disable the first option in a dropdown menu - https://www.w3schools.com/jsref/prop_option_disabled.asp
				document.getElementById("direction").options[0].disabled = true;
                
                // Populate direction with the correct values
				$.each(data.selectDirection, function(selectDirection, value) {
					direction.append($('<option>', {
						value: value,
						text: value
					}, '</option>'));
				});
				direction.removeAttr('disabled');
			})
		}
		// Call function to update the direction dropdown menu
		updateDirection();
	}, 1500);
}

function getStops() {
	console.log("Functon triggered, getting stops");
	//clearTimeout(delayTimer);
	//	delayTimer = setTimeout(function() {
	var origin = $('#origin'),
		destination = $('#destination'),
		direction = $('#direction');
	console.log("The direction is " + direction.val());

	function updateStops() {
		// This will update the origin stop list corresponding to whatever route is typed in
		updateStopSettings();
	}
	//function updateDestinationStops() {
	// This will update the destination stop list corresponding to whatever route is typed in - this may not be necessary in the end - origin and destination will have the same stops so may only need to have one function rather than 2
	//	updateSettings();
	//}
	// Make the selections disabled while fetching new data
	origin.attr('disabled', true);
	destination.attr('disabled', true);

	function updateStopSettings() {
		//route = document.getElementById("route").value;
		var jqxhr = $.getJSON("http://127.0.0.1:5000/stops?direction=" + direction.val(), null, function(data) {
			// Populate the origin stops
			origin.empty();
			$.each(data.originStops, function(originStops, value) {
				origin.append($('<option>', {
					value: value,
					text: value
				}, '</option>'));
			});
			// Populate destination stops
			destination.empty();
			$.each(data.originStops, function(originStops, value) {
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
	updateStops();
	//}, 500);
}

function getLiveWeather() {
	//call weather API from openweathermap - https://openweathermap.org/current and https://openweathermap.org/weather-conditions
	var weatherdata;
	$.getJSON('http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=9ce0d37e8c0ceb69395465d3d9ea6594', function(data) {
		var currentWeather = data.weather[0].description;
		var current_temp = data.main.temp;
		var wind_speed = data.wind.speed;
		var icon = ("<img src='http://openweathermap.org/img/w/" + data.weather[0].icon + ".png'>");
		document.getElementById("weather").innerHTML = current_temp + " &#8451 <br>" + currentWeather + "<br>" + wind_speed + " m/s <br>" + icon;
	})
}

// Ideas for using night mode adapted from - https://stackoverflow.com/questions/4358155/changing-background-based-on-time-of-day-using-javascript
// This is a dynamic function which automatically sets the page to night mode if between 9pm and 6am
function DayNight_Mode() {
	var currentTime = new Date().getHours();
	if (6 <= currentTime && currentTime < 21) {
		document.getElementById('pagestyle').setAttribute('href', '/static/mainStyle.css');
	} else {
		document.getElementById('pagestyle').setAttribute('href', '/static/nightMode.css');
	}
}

// Ideas for changing what CSS file is linked adapted from - http://www.developphp.com/video/JavaScript/Change-Style-Sheet-Using-Tutorial-CSS-Swap-Stylesheet
function toggleNightMode() {
	if (document.getElementById("toggle").checked) {
		document.getElementById('pagestyle').setAttribute('href', '/static/nightMode.css');
	} else {
		document.getElementById('pagestyle').setAttribute('href', '/static/mainStyle.css');
	}
}


// Code for datePicker adapted from
// Code for clockpicker adapted from https://weareoutman.github.io/clockpicker/
$(function() {
	$('#datePicker').datetimepicker({
		format: 'L',
		format: 'DD/MM/YYYY',
	});
});
$(function() {
	$('.clockpicker').clockpicker({
		placement: 'bottom',
		align: 'left',
		autoclose: true,
		'default': 'now'
	});
});


$(document).ready(function() {
	// Automatically trigger DayNight_Mode()
	DayNight_Mode();
});