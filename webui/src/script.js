var currentStockPrice = 178.97,
	currentStockTicker = 'AAPL';
var values = {
	isEnabled: {
		'reddit-sentiment': true,
		'open-close-ratio': true,
		'volume-increase': true,
		'yesterday': true
	},
	indicators: {
		'reddit-sentiment': 0.634,
		'open-close-ratio': 0.33,
		'volume-increase': 0.42,
		'yesterday': 0.9
	},
	trackbars: {
		'reddit-sentiment': 5,
		'open-close-ratio': 5,
		'volume-increase': 5,
		'yesterday': 5
	}
};
// set values
for (var indicatorName in values.indicators) {
	if (values.indicators.hasOwnProperty(indicatorName)) {
		if (values.isEnabled[indicatorName]) {
			$('.' + indicatorName + ' input[type="checkbox"]').prop('checked', true);
		} else {
			$('.' + indicatorName + ' input[type="checkbox"]').prop('checked', false);
		}
		$('.' + indicatorName + ' .indicatorValue').html(values.indicators[indicatorName]);
		indicatorChanged(indicatorName);
	}
}



var isAnalyzing = false;
function startAnalyzing() {
	$('.fourth.indicators input[type="range"]').prop('disabled', true);
	simulation();
	$('#simulationButton').html('Stop Simulations');
	$('#placeholder-img').show();
}
function stopAnalyzing() {
	$('.fourth.indicators input[type="range"]').prop('disabled', false);
	$('#simulationButton').html('Run Simulations');
}


function doMath() {
	// average indicator values
	var numerator = 0,
		denominator = 0;
	for (var indicatorName in values.indicators) {
		if (values.indicators.hasOwnProperty(indicatorName)) {
			var value = values.indicators[indicatorName],
				weight = values.trackbars[indicatorName],
				isEnabled = values.isEnabled[indicatorName];
			if (isEnabled && weight > 0) {
				numerator += values.indicators[indicatorName] * values.trackbars[indicatorName];
				denominator += values.trackbars[indicatorName];
			}
		}
	}
	if (denominator > 0) {
		var averageIndicatorValue = numerator / denominator;
		$('#averageIndicatorValue').html(Math.round(averageIndicatorValue * 100000) / 100000);
		// multiply by money
		var cashToSpend = parseFloat($('#spendableCash').val().replace(/\D/g,'')) * averageIndicatorValue;
		cashToSpend = Math.round(cashToSpend * 100) / 100
		$('#cashToSpend').html('$' + cashToSpend);
		// divide to get stocks
		var numberOfStocksToBuy = Math.floor(cashToSpend / currentStockPrice);
		var numberOfStocksToBuyText;
		if (numberOfStocksToBuy == 0) {
			numberOfStocksToBuyText = "Don't buy "+currentStockTicker+".";
		} else if (numberOfStocksToBuy == 1) {
			numberOfStocksToBuyText = 'Buy ' + numberOfStocksToBuy.toString() + ' share of ' + currentStockTicker;
		} else {
			numberOfStocksToBuyText = 'Buy ' + numberOfStocksToBuy.toString() + ' shares of ' + currentStockTicker;
		}
		$('#theMove').html(numberOfStocksToBuyText);
	} else {
		$('#averageIndicatorValue').html('');
		$('#cashToSpend').html('');
		$('#theMove').html('');
	}
}
doMath();

function indicatorChanged(indicator) {
	// get values
	var indicatorValue = parseFloat($('.' + indicator + ' .indicatorValue').html());
	var trackbarValue = parseFloat($('#' + indicator).val());
	// update values
	values.trackbars[indicator] = trackbarValue;
	$('.' + indicator + ' .trackbarValue').html(trackbarValue);
	doMath();
}
function indicatorCheckbox(indicator) {
	if ($('.' + indicator + ' input[type="checkbox"]').is(':checked')) {
		values.isEnabled[indicator] = true;
		$('.' + indicator + ' .indicatorMath').show();
	} else {
		values.isEnabled[indicator] = false;
		$('.' + indicator + ' .indicatorMath').hide();
	}
	doMath();
}

function indicator() {
	var indicator = 'reddit-sentiment',
		stock = $('#stock').val();

	$.ajax({
		type: 'POST',
		url: 'https://api.stocks.vision/indicator',
		data: { 
			'indicator': indicator, 
			'stock': stock
		},
		success: function(value){
			$('.' + indicator + ' .indicatorValue').html(value);
		}
	});
}


function simulation() {
	var stock = $('#stock').val(),
		holdDuration = $('#holdDuration').val(),
		indicators = {}
		completedSimulations = '';

	$.ajax({
		type: 'POST',
		url: 'https://api.stocks.vision/simulation',
		data: { 
			'stock': stock,
			'holdDuration': holdDuration, 
			'indicators': indicators,
			'completedSimulations': completedSimulations
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
$("#simulationButton").click(function() {
	if (isAnalyzing == true) {
		isAnalyzing = false;
		stopAnalyzing();
	} else {
		isAnalyzing = true;
		startAnalyzing();
	}
});


$('.indicators input[type="range"]').change(function() {
	indicator();
})
