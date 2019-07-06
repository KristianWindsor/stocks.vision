//

var listOfAllStocks = [];

var settings = {
	stock: {
		ticker: 'AAPL',
		price: 178.97
	},
	simulation: {
		length: 3,
		sellStrategy: 0,
		sellTimePeriod: '1 week'
	},
	spendableCash: '$1000',
	isAnalyzing: false
};
var indicators = {
/*	'example': {
		isEnabled: true,
		value: undefined,
		weight: 5
	}*/
};
var simulations = {
	// stockTicker: { "1": {}, "55": {} }
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
	GETindicator('*');
	$.ajax({
		type: 'GET',
		url: 'https://api.stocks.vision/tickerlist',
		success: function(returnData){
			listOfAllStocks = returnData;
		}
	});
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
		$('.fourth.output h2').html('Results for ' + settings.stock.ticker);
		var averageIndicatorValue = numerator / denominator;
		$('#averageIndicatorValue').html((Math.round(averageIndicatorValue * 10) / 10) + '%');
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
		$('#averageIndicatorValue').html('0%');
		$('#cashToSpend').html('$0');
		$('#theMove').html('Nothing.');
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
		GETindicator(indicatorName)
		indicators[indicatorName].isEnabled = true;
	} else {
		indicators[indicatorName].isEnabled = false;
	}
	doMath();
}

function checkForIndicatorUpdate() {
	// stock
	var stock = $('#stock').val().toUpperCase();
	if (listOfAllStocks.indexOf(stock) !== -1 && settings.stock.ticker !== stock) {
		settings.stock.ticker = stock;
		GETindicator('*');
	}
	// hold duration
	// simulation duration
	// spendable cash
	// stock price update
	// enable indicator
	if (true == false) {
		for (var indicatorName in indicators) {
			GETindicator(indicatorName);
		}
	}
}
function GETindicator(indicator) {
	var stock = $('#stock').val().toUpperCase();
	$.ajax({
		type: 'POST',
		url: 'https://api.stocks.vision/indicator',
		data: JSON.stringify({ 
			'indicator': indicator, 
			'stock': stock,
			'date': today
		}),
		contentType: "application/json",
		success: function(returnData){
			console.log(returnData);
			Object.keys(returnData).forEach(function(indicatorName) {
				// update value
				if (!indicators.hasOwnProperty(indicatorName)) {
					indicators[indicatorName] = {
						isEnabled: true,
						value: returnData[indicatorName],
						weight: 5
					};
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
							<span class="indicatorValue">`+(Math.round(returnData[indicatorName] * 10) / 10)+`%</span> * <span class="trackbarValue">`+indicators[indicatorName].weight+`</span>
						</div>
			 		`;
			 		$('.fourth.indicators').append(html);
				} else {
					$('.'+indicatorName+' .indicatorValue').html((Math.round(returnData[indicatorName] * 10) / 10) + '%');
				}
			});
			// update math
			doMath();
		}
	});
}


function simulation() {
	var stock = $('#stock').val().toUpperCase(),
		length = settings.simulation.length,
		simID = stock,
		completedSimulations = {};
		if (simulations[simID] && simulations[simID][length]) {
			completedSimulations = simulations[simID][length];
		}

	$.ajax({
		type: 'POST',
		url: 'https://api.stocks.vision/simulation',
		data: JSON.stringify({ 
			'stock': stock,
			'length': length, 
			'indicators': indicators,
			'completedSimulations': completedSimulations
		}),
		dataType: 'json',
		contentType: "application/json",
		success: function(returnData){
			console.log(returnData);
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
