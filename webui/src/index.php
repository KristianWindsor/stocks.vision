<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<title>
			Stocks Vision
		</title>
		<link rel="stylesheet" href="style.css">
		<meta name="description" content="Stocks Vision">
		<meta name="viewport" content="width=device-width,initial-scale=1.0">
		<link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
	</head>
	<body><!--
	 --><div class="fourth input">
			<h1>
				Stocks Vision
			</h1>
			<div>
				<span>Stock</span><br>
				<input id="stock" type="text" value="" onchange="stockInputChanged()" />
			</div>
			<button id="simulationButton">
				Run Stock Analysis
			</button>
		</div><!--
	 --><div class="fourth output">
			<div>
				<h2>Results</h2>
				<p>
					Indicator Value (Averaged)<br>
					<span id="averageIndicatorValue" class="result"></span>
				</p>
				<p>
					Cash to Spend<br>
					<input id="spendableCash" type="text" value="" onchange="checkForIndicatorUpdate()" />
					<br>
					<span id="cashToSpend" class="result"></span>
				</p>
				<p>
					The move<br>
					<span id="theMove" class="result"></span>
				</p>
			</div>
		</div><!--
	 --><div class="fourth indicators">
			<h2>Indicators</h2>
		</div><!--
	 --><div class="fourth simulations">
			<div>
				<h2>Simulation</h2>
				<p>
					Length of simulation in weeks:
				</p>
				<table>
					<tbody>
						<tr class="timepicker">
							<td>
								<a onclick="setSimulationLength(1)" class="tp1">1 Week</a>
							</td>
							<td>
								<a onclick="setSimulationLength(2)" class="tp2">2 Weeks</a>
							</td>
							<td>
								<a onclick="setSimulationLength(4)" class="tp4">1 Month</a>
							</td>
							<td>
								<a onclick="setSimulationLength(13)" class="tp13">3 Months</a>
							</td>
							<td>
								<a onclick="setSimulationLength(26)" class="tp26">6 Months</a>
							</td>
							<td>
								<a onclick="setSimulationLength(52)" class="tp52">1 Year</a>
							</td>
							<td>
								<a onclick="setSimulationLength(104)" class="tp104">2 Years</a>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="chart-wrap">
					<canvas id="chartPrices" width="400" height="400"></canvas>
					<canvas id="chartHoldings" width="400" height="400"></canvas>
					<canvas id="chartIndicators" width="400" height="400"></canvas>
				</div>
				<div class="transactions">
					<table>
						<tbody id="transactions">
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</body>
	<script type="text/javascript" src="jquery-3.5.1.min.js"></script>
	<script type="text/javascript" src="moment.min.js"></script>
	<script type="text/javascript" src="Chart.min.js"></script>
	<script>
		var API_URL = '<?php echo getenv('API_URL'); ?>';
	</script>
	<script type="text/javascript" src="script.js"></script>
</html>