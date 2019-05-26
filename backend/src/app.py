#!/usr/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import indicators.example

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#
# index
#
@app.route('/')
def index():
    return "Hey! You're not supposed to be here!"


#
# indicator
#
@app.route('/indicator', methods=["POST"])
@cross_origin()
def indicator():
	indicator = request.form.get('indicator')
	stock = request.form.get('stock')
	# run indicator py script with given stock
	# return results
	results = indicators.example.main('AAPL')
	return results


#
# simulation
#
@app.route('/simulation', methods=["POST"])
@cross_origin()
def simulation():
	stock = request.form.get('stock')
	holdDuration = request.form.get('holdDuration')
	indicators = request.form.get('indicators')
	completedSimulations = request.form.get('completedSimulations')
	# calculate which simulations to run based off of completedSimulations
	# run simulation
	# return results
	return '200 OK'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)