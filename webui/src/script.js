//

var listOfAllStocks = [];

var settings = {
	stock: {
		ticker: 'AAPL',
		price: 178.97
	},
	backtest: {
		length: 4
	},
	strategies: { /*
		strategyName: {
			isEnabled: true,
			value: 0.618,
			weight: 5 
		}*/
	},
	spendableCash: '$1000'
};
var backtestData = { /*
	stockID: {
		strategyConfigID: {
			backtestDuration: data
		}
	} */
};

var chartStrategies,
	chartHoldings,
	chartPrices;

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();
today = yyyy + '-' + mm + '-' + dd;



// set values
function initializeHTML() {
	$('#stock').val(settings.stock.ticker);
	$('#spendableCash').val(settings.spendableCash);
	$('.tp' + settings.backtest.length.toString()).addClass('picked');
	GETstrategy(settings.stock.ticker, '*');
	$.ajax({
		type: 'GET',
		url: API_URL + '/tickerlist',
		success: function(returnData){
			listOfAllStocks = returnData;
		}
	});
	function chartOptions(chartName) {
		var tickLabel,
			timeUnit;
		if (chartName === 'holdings') {
			tickLabel = ' shares';
		} else {
			tickLabel = '%'
		}
		if (settings.backtest.length < 6) {
			timeUnit = 'day';
		} else if (settings.backtest.length < 52) {
			timeUnit = 'week';
		} else if (settings.backtest.length >= 52) {
			timeUnit = 'month';
		}
		return {
			responsive: true,
			maintainAspectRatio: false,
			legend: {
				display: true
			},
			scales: {
				xAxes: [{
					type: 'time',
					distribution: 'linear',
					time: {
						unit: timeUnit,
						unitStepSize: 1
					}
				}],
				yAxes: [{
					ticks: {
						callback: function (value) {
							return value + tickLabel;
						}
					}
				}]
			}
		};
	}
	var canvasPrices = document.getElementById("chartPrices");
	chartPrices = new Chart(canvasPrices.getContext("2d"), {
		type: 'line',
		data: {
			datasets: [{
				label: 'Portfolio Net Worth',
				data: [],
				backgroundColor: 'rgb(33, 206, 153, 0.2)',
				borderColor: 'rgb(33, 206, 153, 1)'
			}, {
				label: settings.stock.ticker + ' Price',
				data: [],
				backgroundColor: 'rgb(206, 153, 33, 0)',
				borderColor: 'rgb(206, 153, 33, 1)'
			}]
		},
		options: chartOptions('prices')
	});
	var canvasHoldings = document.getElementById("chartHoldings");
	chartHoldings = new Chart(canvasHoldings.getContext("2d"), {
		type: 'line',
		data: {
			datasets: [{
				label: settings.stock.ticker + ' Shares',
				data: [],
				backgroundColor: 'rgb(33, 206, 153, 0.2)',
				borderColor: 'rgb(33, 206, 153, 1)'
			}]
		},
		options: chartOptions('holdings')
	});
	var canvasStrategies = document.getElementById("chartStrategies");
	chartStrategies = new Chart(canvasStrategies.getContext("2d"), {
		type: 'line',
		data: {
			datasets: []
		},
		options: chartOptions('strategies')
	});
}


function doMath() {
	// average strategy values
	var numerator = 0,
		denominator = 0;
	for (var strategyName in settings.strategies) {
		if (settings.strategies.hasOwnProperty(strategyName)) {
			var value = settings.strategies[strategyName].value,
				weight = settings.strategies[strategyName].weight,
				isEnabled = settings.strategies[strategyName].isEnabled;
			if (isEnabled && weight > 0 && value) {
				numerator += value * weight;
				denominator += weight;
			}
		}
	}

	if (denominator > 0) {
		$('.fourth.output h2').html('Results for ' + settings.stock.ticker);
		var averageStrategyValue = numerator / denominator;
		$('#averageStrategyValue').html((Math.round(averageStrategyValue * 10) / 10) + '%');
		// multiply by money
		var cashToSpend = parseFloat($('#spendableCash').val().replace(/\D/g,'')) * (averageStrategyValue / 100);
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
		$('#averageStrategyValue').html('0%');
		$('#cashToSpend').html('$0');
		$('#theMove').html('Nothing.');
	}
}

function strategyWeightChanged(strategyName) {
	// get values
	var strategyValue = parseFloat($('.' + strategyName + ' .strategyValue').html());
	var trackbarValue = parseFloat($('#' + strategyName).val());
	// update values
	settings.strategies[strategyName].weight = trackbarValue;
	$('.' + strategyName + ' .trackbarValue').html(trackbarValue);
	backtest();
	doMath();
}
function strategyEnabledChanged(strategyName) {
	if ($('.' + strategyName + ' input[type="checkbox"]').is(':checked')) {
		GETstrategy(settings.stock.ticker, strategyName)
		settings.strategies[strategyName].isEnabled = true;
	} else {
		settings.strategies[strategyName].isEnabled = false;
		backtest();
	}
	doMath();
}

function stockInputChanged() {
	var stock = $('#stock').val().toUpperCase();
	if (listOfAllStocks.indexOf(stock) !== -1 && settings.stock.ticker !== stock) {
		settings.stock.ticker = stock;
		GETstrategy(stock, '*');
	}
}
function GETstrategy(stock, strategy) {
	$.ajax({
		type: 'POST',
		url: API_URL + '/strategy',
		data: JSON.stringify({ 
			'strategy': strategy,
			'stock': stock,
			'date': today
		}),
		contentType: "application/json",
		success: function(returnData){
			Object.keys(returnData).forEach(function(strategyName) {
				// update value
				if (!settings.strategies.hasOwnProperty(strategyName)) {
					settings.strategies[strategyName] = {
						isEnabled: true,
						value: returnData[strategyName],
						weight: 1
					};
				} else {
					settings.strategies[strategyName].value = returnData[strategyName];
				}
				// populate html
				if (!$('.'+strategyName).length) {
					var checkboxMaybeChecked = '';
					if (settings.strategies[strategyName].isEnabled == true) {
						checkboxMaybeChecked = 'checked="checked"';
					}
					var html = `
						<div class="`+strategyName+`">
							<input type="checkbox" onchange="strategyEnabledChanged('`+strategyName+`')" `+checkboxMaybeChecked+` /><br>
							`+strategyName+`
							<input id="`+strategyName+`" type="range" min="-5" max="5" value="`+settings.strategies[strategyName].weight+`" oninput="strategyWeightChanged('`+strategyName+`');" />
							<span class="strategyValue">`+(Math.round(returnData[strategyName] * 10) / 10)+`%</span> * <span class="trackbarValue">`+settings.strategies[strategyName].weight+`</span>
						</div>
					`;
					$('.fourth.strategies').append(html);
				} else {
					$('.'+strategyName+' .strategyValue').html((Math.round(returnData[strategyName] * 10) / 10) + '%');
				}
			});
			// update math
			doMath();
			// update backtest
			backtest();
		}
	});
}

function generateStrategyConfigID(strategies) {
	var strategyConfigID = '';
	for (var strategyName in strategies) {
		if (strategies.hasOwnProperty(strategyName)) {
			if (strategies[strategyName] != 0) {
				strategyConfigID += strategyName;
				if (strategies.length != 1) {
					strategyConfigID += strategies[strategyName];
				}
			}
		}
	}
	return strategyConfigID;
}
function getStrategySettings() {
	var strategySettings = {};
	for (var key in settings.strategies) {
		if (settings.strategies.hasOwnProperty(key)) {
			if (settings.strategies[key]['isEnabled'] && settings.strategies[key]['weight'] != 0) {
				strategySettings[key] = settings.strategies[key]['weight'];
			}
		}
	}
	return strategySettings;
}


function backtest() {
	var stock = settings.stock.ticker,
		length = settings.backtest.length,
		strategySettings = getStrategySettings(),
		strategyConfigID = generateStrategyConfigID(strategySettings);

	if (!backtestData.hasOwnProperty(stock)) {
		backtestData[stock] = {};
	}
	if (!backtestData[stock].hasOwnProperty(strategyConfigID)) {
		backtestData[stock][strategyConfigID] = {};
	}
	if (!backtestData[stock][strategyConfigID].hasOwnProperty(length)) {
		backtestData[stock][strategyConfigID][length] = {};
	}
	if (Object.entries(backtestData[stock][strategyConfigID][length]).length === 0) {
		$.ajax({
			type: 'POST',
			url: API_URL + '/backtest',
			data: JSON.stringify({ 
				'stock': stock,
				'length': length, 
				'strategies': strategySettings
			}),
			contentType: "application/json",
			success: function(returnData){
				backtestData[stock][strategyConfigID][length] = returnData;
				renderChart(returnData);
			}
		});
	} else {
		renderChart(backtestData[stock][strategyConfigID][length]);
	}
}

function setBacktestLength(length) {
	settings.backtest.length = length;
	$('.timepicker a').removeClass('picked');
	$('.tp' + length.toString()).addClass('picked');
	backtest();
}

function randomNum(min,max) {
    return Math.floor(Math.random()*(max-min+1)+min).toString();
}

function renderChart(allData) {
	var chartData = [],
		stockChartData = [],
		stockQuantityData = [],
		strategyDataSets = [],
		strategyData = {};
	for (var key in allData['chartData']) {
		if (allData['chartData'].hasOwnProperty(key)) {
			chartData.push({
				x: new Date(key),
				y: allData['chartData'][key]['portfolioNetWorthPercent']
			});
			stockChartData.push({
				x: new Date(key),
				y: allData['chartData'][key]['stockPricePercent']
			});
			stockQuantityData.push({
				x: new Date(key),
				y: allData['chartData'][key]['stockQuantity']
			});
			
			for (var strategyName in allData['chartData'][key]['strategies']) {
				if (allData['chartData'][key]['strategies'].hasOwnProperty(strategyName)) {
					if (!strategyData[strategyName]) {
						strategyData[strategyName] = [];
					}
					strategyData[strategyName].push({
						x: new Date(key),
						y: allData['chartData'][key]['strategies'][strategyName]
					});
				}
			}
		}
	}
	for (var strategyName in allData['strategies']) {
		if (allData['strategies'].hasOwnProperty(strategyName)) {
			var color = randomNum(0,255) + ', ' + randomNum(0,255) + ', ' + randomNum(0,255)
			strategyDataSets.push({
				label: strategyName,
				data: strategyData[strategyName],
				backgroundColor: 'rgb('+color+', 0.2)',
				borderColor: 'rgb('+color+', 1)'
			});
		}
	}
	if (settings.backtest.length < 6) {
		timeUnit = 'day';
	} else if (settings.backtest.length < 52) {
		timeUnit = 'week';
	} else if (settings.backtest.length >= 52) {
		timeUnit = 'month';
	}

	chartPrices.options.scales.xAxes[0].time.unit = timeUnit;
	chartPrices.data.datasets[1].label = settings.stock.ticker + ' Price';
	chartPrices.data.datasets[0].data = chartData;
	chartPrices.data.datasets[1].data = stockChartData;
	chartPrices.update();
	chartHoldings.options.scales.xAxes[0].time.unit = timeUnit;
	chartHoldings.data.datasets[0].label = settings.stock.ticker + ' Shares';
	chartHoldings.data.datasets[0].data = stockQuantityData;
	chartHoldings.update();
	chartStrategies.options.scales.xAxes[0].time.unit = timeUnit;
	chartStrategies.data.datasets = strategyDataSets;
	chartStrategies.update();
}


initializeHTML();



$('#stock').on('input', function() {
	// if ($(this).val().length > 0) {
	// 	backtest();
	// }
});
$('#holdDuration').on('input', function() {
	if ($(this).val().length > 0) {
		backtest();
	}
});
$('#spendableCash').on('input', function() {
	if ($(this).val().length > 0) {
		doMath();
	}
});
