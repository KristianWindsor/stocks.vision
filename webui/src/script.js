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
	indicators: { /*
		indicatorName: {
			isEnabled: true,
			value: 0.618,
			weight: 5 
		}*/
	},
	spendableCash: '$1000'
};
var backtestData = { /*
	stockID: {
		indicatorConfigID: {
			backtestDuration: data
		}
	} */
};

var chartIndicators,
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
	GETindicator(settings.stock.ticker, '*');
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
	var canvasIndicators = document.getElementById("chartIndicators");
	chartIndicators = new Chart(canvasIndicators.getContext("2d"), {
		type: 'line',
		data: {
			datasets: []
		},
		options: chartOptions('indicators')
	});
}


function doMath() {
	// average indicator values
	var numerator = 0,
		denominator = 0;
	for (var indicatorName in settings.indicators) {
		if (settings.indicators.hasOwnProperty(indicatorName)) {
			var value = settings.indicators[indicatorName].value,
				weight = settings.indicators[indicatorName].weight,
				isEnabled = settings.indicators[indicatorName].isEnabled;
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
	settings.indicators[indicatorName].weight = trackbarValue;
	$('.' + indicatorName + ' .trackbarValue').html(trackbarValue);
	backtest();
	doMath();
}
function indicatorEnabledChanged(indicatorName) {
	if ($('.' + indicatorName + ' input[type="checkbox"]').is(':checked')) {
		GETindicator(settings.stock.ticker, indicatorName)
		settings.indicators[indicatorName].isEnabled = true;
	} else {
		settings.indicators[indicatorName].isEnabled = false;
		backtest();
	}
	doMath();
}

function stockInputChanged() {
	var stock = $('#stock').val().toUpperCase();
	if (listOfAllStocks.indexOf(stock) !== -1 && settings.stock.ticker !== stock) {
		settings.stock.ticker = stock;
		GETindicator(stock, '*');
	}
}
function GETindicator(stock, indicator) {
	$.ajax({
		type: 'POST',
		url: API_URL + '/indicator',
		data: JSON.stringify({ 
			'indicator': indicator,
			'stock': stock,
			'date': today
		}),
		contentType: "application/json",
		success: function(returnData){
			Object.keys(returnData).forEach(function(indicatorName) {
				// update value
				if (!settings.indicators.hasOwnProperty(indicatorName)) {
					settings.indicators[indicatorName] = {
						isEnabled: true,
						value: returnData[indicatorName],
						weight: 1
					};
				} else {
					settings.indicators[indicatorName].value = returnData[indicatorName];
				}
				// populate html
				if (!$('.'+indicatorName).length) {
					var checkboxMaybeChecked = '';
					if (settings.indicators[indicatorName].isEnabled == true) {
						checkboxMaybeChecked = 'checked="checked"';
					}
					var html = `
						<div class="`+indicatorName+`">
							<input type="checkbox" onchange="indicatorEnabledChanged('`+indicatorName+`')" `+checkboxMaybeChecked+` /><br>
							`+indicatorName+`
							<input id="`+indicatorName+`" type="range" min="-5" max="5" value="`+settings.indicators[indicatorName].weight+`" oninput="indicatorWeightChanged('`+indicatorName+`');" />
							<span class="indicatorValue">`+(Math.round(returnData[indicatorName] * 10) / 10)+`%</span> * <span class="trackbarValue">`+settings.indicators[indicatorName].weight+`</span>
						</div>
					`;
					$('.fourth.indicators').append(html);
				} else {
					$('.'+indicatorName+' .indicatorValue').html((Math.round(returnData[indicatorName] * 10) / 10) + '%');
				}
			});
			// update math
			doMath();
			// update backtest
			backtest();
		}
	});
}

function generateIndicatorConfigID(indicators) {
	var indicatorConfigID = '';
	for (var indicatorName in indicators) {
		if (indicators.hasOwnProperty(indicatorName)) {
			if (indicators[indicatorName] != 0) {
				indicatorConfigID += indicatorName;
				if (indicators.length != 1) {
					indicatorConfigID += indicators[indicatorName];
				}
			}
		}
	}
	return indicatorConfigID;
}
function getIndicatorSettings() {
	var indicatorSettings = {};
	for (var key in settings.indicators) {
		if (settings.indicators.hasOwnProperty(key)) {
			if (settings.indicators[key]['isEnabled'] && settings.indicators[key]['weight'] != 0) {
				indicatorSettings[key] = settings.indicators[key]['weight'];
			}
		}
	}
	return indicatorSettings;
}


function backtest() {
	var stock = settings.stock.ticker,
		length = settings.backtest.length,
		indicatorSettings = getIndicatorSettings(),
		indicatorConfigID = generateIndicatorConfigID(indicatorSettings);

	if (!backtestData.hasOwnProperty(stock)) {
		backtestData[stock] = {};
	}
	if (!backtestData[stock].hasOwnProperty(indicatorConfigID)) {
		backtestData[stock][indicatorConfigID] = {};
	}
	if (!backtestData[stock][indicatorConfigID].hasOwnProperty(length)) {
		backtestData[stock][indicatorConfigID][length] = {};
	}
	if (Object.entries(backtestData[stock][indicatorConfigID][length]).length === 0) {
		$.ajax({
			type: 'POST',
			url: API_URL + '/backtest',
			data: JSON.stringify({ 
				'stock': stock,
				'length': length, 
				'indicators': indicatorSettings
			}),
			contentType: "application/json",
			success: function(returnData){
				backtestData[stock][indicatorConfigID][length] = returnData;
				renderChart(returnData);
			}
		});
	} else {
		renderChart(backtestData[stock][indicatorConfigID][length]);
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
		indicatorDataSets = [],
		indicatorData = {};
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
			
			for (var indicatorName in allData['chartData'][key]['indicators']) {
				if (allData['chartData'][key]['indicators'].hasOwnProperty(indicatorName)) {
					if (!indicatorData[indicatorName]) {
						indicatorData[indicatorName] = [];
					}
					indicatorData[indicatorName].push({
						x: new Date(key),
						y: allData['chartData'][key]['indicators'][indicatorName]
					});
				}
			}
		}
	}
	for (var indicatorName in allData['indicators']) {
		if (allData['indicators'].hasOwnProperty(indicatorName)) {
			var color = randomNum(0,255) + ', ' + randomNum(0,255) + ', ' + randomNum(0,255)
			indicatorDataSets.push({
				label: indicatorName,
				data: indicatorData[indicatorName],
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
	chartIndicators.options.scales.xAxes[0].time.unit = timeUnit;
	chartIndicators.data.datasets = indicatorDataSets;
	chartIndicators.update();
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
