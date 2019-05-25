
var isAnalyzing = true;
function startAnalyzing() {
	$('.fourth.indicators input[type="range"]').prop('disabled', true);
	simulation();
	$('#analyze').html('Stop Analyzing');
}
function stopAnalyzing() {
	$('.fourth.indicators input[type="range"]').prop('disabled', false);
	$('#analyze').html('Start Analyzing');
}


function doMath() {
	// list of indicator values
	// average
	// multiply by money
	// divide to get stocks
	// output results
}

function indicator() {
	var indicator,
		stock = $('#stock').val();

	$.ajax({
		type: 'POST',
		url: 'https://api.stocks.vision/indicator',
		data: { 
			'indicator': indicator, 
			'stock': stock
		},
		success: function(msg){
			console.log("horray! " + msg);
		}
	});
}


function simulation() {
	var stock = $('#stock').val(),
		holdDuration = $('#holdDuration').val(),
		indicators = {};

	$.ajax({
		type: 'POST',
		url: 'https://api.stocks.vision/simulation',
		data: { 
			'stock': stock,
			'holdDuration': holdDuration, 
			'indicators': indicators
		},
		success: function(msg){
			console.log("horray! " + msg);
		}
	});
}


$('#stock').on('input', function() {
	if ($(this).val().length > 0) {
		simulation();
	}
});
$('#holdDuration').on('input', function() {
	if ($(this).val().length > 0) {
		simulation();
	}
});
$('#spendableCash').on('input', function() {
	if ($(this).val().length > 0) {
		doMath();
	}
});
$("#analyze").click(function() {
	if (isAnalyzing == true) {
		isAnalyzing = false;
		stopAnalyzing();
	} else {
		isAnalyzing = true;
		startAnalyzing();
	}
});

startAnalyzing();