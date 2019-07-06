//

var settings = {
	stock: {
		ticker: 'AAPL',
		price: 178.97
	},
	simulation: {
		length: '6 months',
		sellStrategy: 0,
		sellTimePeriod: '1 week'
	},
	spendableCash: '$1000',
	isAnalyzing: false
};
var indicators = {
	'reddit-wallstreetbets': {
		isEnabled: true,
		value: undefined,
		weight: 5
	},
	'reddit-stocks': {
		isEnabled: true,
		value: undefined,
		weight: 5
	},
	'volume-increase': {
		isEnabled: true,
		value: undefined,
		weight: 5
	},
	'example': {
		isEnabled: true,
		value: undefined,
		weight: 5
	}
};

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();
today = yyyy + '-' + mm + '-' + dd;

// set values
function initializeHTML() {
	$('#stock').val(settings.stock.ticker);
	$('#holdDuration').val(settings.simulation.sellTimePeriod);
	if (settings.simulation.sellStrategy == 0) {
		$('#sell-indicators').prop("checked", true);
	} else {
		$('#sell-time').prop("checked", true);
	}
	$('#simulationDuration').val(settings.simulation.length);
	$('#spendableCash').val(settings.spendableCash);
	for (var indicatorName in indicators) {
		if (indicators.hasOwnProperty(indicatorName)) {
			if (indicators[indicatorName].isEnabled) {
				$('.' + indicatorName + ' input[type="checkbox"]').prop('checked', true);
			} else {
				$('.' + indicatorName + ' input[type="checkbox"]').prop('checked', false);
			}
			indicatorWeightChanged(indicatorName);
		}
	}
			console.log('GET:' + indicatorName)
	GETindicator('*');
}

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
	for (var indicatorName in indicators) {
		if (indicators.hasOwnProperty(indicatorName)) {
			var value = indicators[indicatorName].value,
				weight = indicators[indicatorName].weight,
				isEnabled = indicators[indicatorName].isEnabled;
			if (isEnabled && weight > 0 && value) {
				numerator += value * weight;
				denominator += weight;
			}
		}
	}

	if (denominator > 0) {
		var averageIndicatorValue = numerator / denominator;
		$('#averageIndicatorValue').html((Math.round(averageIndicatorValue * 100000) / 100000) + '%');
		// multiply by money
		var cashToSpend = parseFloat($('#spendableCash').val().replace(/\D/g,'')) * (averageIndicatorValue / 100);
		cashToSpend = Math.round(cashToSpend * 100) / 100
		$('#cashToSpend').html('$' + cashToSpend);
		// divide to get stocks
		var numberOfStocksToBuy = Math.floor(cashToSpend / settings.stock.price);
		var numberOfStocksToBuyText;
		if (numberOfStocksToBuy == 0) {
			numberOfStocksToBuyText = "Don't buy "+settings.stock.ticker+".";
		} else if (numberOfStocksToBuy == 1) {
			numberOfStocksToBuyText = 'Buy ' + numberOfStocksToBuy.toString() + ' share of ' + settings.stock.ticker;
		} else {
			numberOfStocksToBuyText = 'Buy ' + numberOfStocksToBuy.toString() + ' shares of ' + settings.stock.ticker;
		}
		$('#theMove').html(numberOfStocksToBuyText);
	} else {
		$('#averageIndicatorValue').html('');
		$('#cashToSpend').html('');
		$('#theMove').html('');
	}
}

function indicatorWeightChanged(indicatorName) {
	// get values
	var indicatorValue = parseFloat($('.' + indicatorName + ' .indicatorValue').html());
	var trackbarValue = parseFloat($('#' + indicatorName).val());
	// update values
	if (trackbarValue >= 0 && trackbarValue <= 10) {
		indicators[indicatorName].weight = trackbarValue;
		$('.' + indicatorName + ' .trackbarValue').html(trackbarValue);
	}
	doMath();
}
function indicatorEnabledChanged(indicatorName) {
	if ($('.' + indicatorName + ' input[type="checkbox"]').is(':checked')) {
			console.log('GET:' + indicatorName)
		GETindicator(indicatorName)
		indicators[indicatorName].isEnabled = true;
	} else {
		indicators[indicatorName].isEnabled = false;
	}
	doMath();
}

function checkForIndicatorUpdate() {
	// stock
	// hold duration
	// simulation duration
	// spendable cash
	// stock price update
	// enable indicator
	if (true == false) {
		for (var indicatorName in indicators) {
			console.log('GET:' + indicatorName)
			GETindicator(indicatorName);
		}
	}
}
function GETindicator(indicator) {
	var stock = $('#stock').val();
	$.ajax({
		type: 'POST',
		url: 'https://api.stocks.vision/indicator',
		data: JSON.stringify({ 
			'indicator': indicator, 
			'stock': stock,
			'date': today
		}),
		// dataType: 'json',
		contentType: "application/json",
		success: function(returnData){
			console.log(returnData);
			Object.keys(returnData).forEach(function(indicatorName) {
				console.log(indicatorName);
				console.log(indicators['0']);
				// update value
				if (!indicators.hasOwnProperty(indicatorName)) {
					indicators[indicatorName] = {
						isEnabled: true,
						value: returnData[indicatorName],
						weight: 5
					};
					console.log(indicators['0']);
				} else {
					indicators[indicatorName].value = returnData[indicatorName];
				}
				// populate html
				if (!$('.'+indicatorName).length) {
					var checkboxMaybeChecked = '';
					if (indicators[indicatorName].isEnabled == true) {
						checkboxMaybeChecked = 'checked="checked"';
					}
			 		var html = `
			 			<div class="`+indicatorName+`">
							<input type="checkbox" onchange="indicatorEnabledChanged('`+indicatorName+`')" `+checkboxMaybeChecked+` /><br>
							`+indicatorName+`
							<input id="`+indicatorName+`" type="range" min="0" max="10" value="`+indicators[indicatorName].weight+`" oninput="indicatorWeightChanged('`+indicatorName+`');" onchange="indicatorWeightChanged('`+indicatorName+`');" />
							<span class="indicatorValue">`+returnData[indicatorName]+`</span> * <span class="trackbarValue">`+indicators[indicatorName].weight+`</span>
						</div>
			 		`;
			 		$('.fourth.indicators').append(html);
				}
			});
			// update math
			doMath();
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
		dataType: 'json',
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



initializeHTML();



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
	if (settings.isAnalyzing == true) {
		settings.isAnalyzing = false;
		stopAnalyzing();
	} else {
		settings.isAnalyzing = true;
		startAnalyzing();
	}
});
