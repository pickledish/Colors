#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os, json, csv
from random import randint

from ColorLogic import Color, Model

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
	db_session.remove()
'''

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():

	sessionID = request.cookies.get('session')
	if sessionID is None: sessionID = str(randint(0, 100000))

	c = Color.random().hexColor
	d = Color.random().hexColor

	resp = make_response(render_template('pages/main.html', color1 = c, color2 = d))
	resp.set_cookie('session', sessionID)

	return resp

@app.route('/handleResponse')
def handler():

	returned1 = Color(request.args.get("color1"))
	returned2 = Color(request.args.get("color2"))
	response = int(request.args.get("response"))

	# numAnswered = int(request.args.get('numAnswered'))
	sessionID = request.cookies.get('session')

	row = returned1.getColorVector() + returned2.getColorVector() + [response]
	backwards = returned2.getColorVector() + returned1.getColorVector() + [response]

	with open('csv/everyone.csv', 'a') as everyone:

		writer = csv.writer(everyone, delimiter = ',')
		writer.writerow(row)
		writer.writerow(backwards)

	with open('csv/' + sessionID + '.csv', 'a') as specific:

		writer = csv.writer(specific, delimiter = ',')
		writer.writerow(row)
		writer.writerow(backwards)

	c = Color.random().hexColor
	d = Color.random().hexColor

	jDict = {'color1': c, 'color2': d, 'sessionID': sessionID}
	return json.dumps(jDict)

@app.route('/results/<sessionID>')
def results(sessionID):

	model = Model(sessionID)
	colorPairs = model.getLikedPairs(3)

	hexPairs = [[pair[0].hexColor, pair[1].hexColor] for pair in colorPairs]

	return render_template('pages/results.html', pairs = hexPairs)

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
	return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404

if not app.debug:
	file_handler = FileHandler('error.log')
	file_handler.setFormatter(
		Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
	)
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
	app.run()

