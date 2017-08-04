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
	}, 2000);
}

function getStops() {
	console.log("Functon triggered, getting stops");
	//clearTimeout(delayTimer);
	var origin = $('#origin'),
		destination = $('#destination'),
		direction = $('#direction');
	console.log("The direction is: " + direction.val());

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
}

function getLiveWeather() {
	//call weather API from openweathermap - https://openweathermap.org/current and https://openweathermap.org/weather-conditions
	var weatherdata;
	$.getJSON('http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=9ce0d37e8c0ceb69395465d3d9ea6594', function(data) {
		var currentWeather = data.weather[0].description;
		var current_temp = data.main.temp;
		var wind_speed = data.wind.speed;
        // Make first letter of currentWeather uppercase
        var currentWeatherFirstLetterUppercase = currentWeather.charAt(0).toUpperCase() + currentWeather.slice(1);
		var icon = ("<img src='http://openweathermap.org/img/w/" + data.weather[0].icon + ".png'>");
		document.getElementById("weather").innerHTML = "The current temperature is: " + current_temp + " &#8451 <br> Windspeeds of: " + wind_speed + " m/s <br> Overall: " + currentWeatherFirstLetterUppercase + icon;
	})
}

// Ideas for using night mode adapted from - https://stackoverflow.com/questions/4358155/changing-background-based-on-time-of-day-using-javascript
// This is a dynamic function which automatically sets the page to night mode if between 9pm and 6am
function DayNight_Mode() {
	var currentTime = new Date().getHours();
	if (6 <= currentTime && currentTime < 22) {
		document.getElementById('pagestyle').setAttribute('href', '/static/mainStyle.css');
	} else {
		document.getElementById('pagestyle').setAttribute('href', '/static/nightMode.css');
        document.getElementById("toggle").checked = true; // make the toggle checked if night mode is running
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


// Code for datePicker adapted from http://eonasdan.github.io/bootstrap-datetimepicker/#bootstrap-3-datepicker-v4-docs
// Disabling dates idea adapted from https://stackoverflow.com/questions/42974011/disable-future-dates-in-bootstrap-3-datetimepicker
// Code for clockpicker adapted from https://weareoutman.github.io/clockpicker/  
$(function() {
	$('#datePicker').datetimepicker({
		format: 'L',
		format: 'DD/MM/YYYY',
        maxDate: moment().add(7, 'days')
	});
});

$(function() {
	$('.clockpicker').clockpicker({
		placement: 'top',
		align: 'left',
		autoclose: true,
		'default': 'now'
	});
});


$(document).ready(function() {
	// Automatically trigger DayNight_Mode()
	DayNight_Mode();
});

// Code to get autocomplete suggestions working adapted from https://jqueryui.com/autocomplete/ and https://stackoverflow.com/questions/9569146/jquery-ui-autocomplete-how-to-trigger-an-event-when-an-item-is-selected

var availableRoutes = ['1', '4', '7', '8', '9', '11', '13', '14', '15', '16', '17', '18', '25', '26', '27', '31', '32', '33', '37', '38', '39', '40', '41', '42', '43', '44', '46', '47', '49', '53', '59', '61', '63', '65', '66', '67', '68', '69', '70', '75', '76', '79', '7B', '7D', '83', '84', '86', '102', '104', '111', '114', '116', '118', '120', '122', '123', '130', '140', '142', '145', '14C', '150', '151', '15A', '15B', '161', '16C', '17A', '184', '185', '220', '236', '238', '239', '25A', '25B', '25X', '270', '27A', '27B', '27X', '29A', '31A', '31B', '32X', '332', '33A', '33B', '33X', '38A', '38B', '39A', '40B', '40D', '41A', '41B', '41C', '41X', '44B', '45A', '46A', '46E', '51D', '51X', '54A', '56A', '65B', '66A', '66B', '66X', '67X', '68A', '69X', '747', '76A', '77A', '79A', '83A', '84A', '84X']

$(function() {
    $( ".route" ).autocomplete({
      source: availableRoutes,
      select: function(event, ui) {
        // Calls the getDirection() function when the user clicks on something from the autocomplete menu - not sure if this is a good idea as could
        // delay user getting the direction information but adds redundancy if the user clicks something after the eventlistener has already
        // gathered the directions for a different stop
        getDirection();
    }
    });
  } );