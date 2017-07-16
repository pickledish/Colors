#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os, json, csv

from ColorLogic import Color

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
	c = Color.random().hexColor
	d = Color.random().hexColor
	return render_template('pages/main.html', color1 = c, color2 = d)

@app.route('/handleResponse')
def handler():

	returned1 = Color(request.args.get("color1"))
	returned2 = Color(request.args.get("color2"))
	response = int(request.args.get("response"))

	row = returned1.getColorVector() + returned2.getColorVector() + [response]
	backwards = row = returned2.getColorVector() + returned1.getColorVector() + [response]

	with open('eggs.csv', 'a') as csvfile:

		spamwriter = csv.writer(csvfile, delimiter = ',')
		spamwriter.writerow(row)
		spamwriter.writerow(backwards)

	c = Color.random().hexColor
	d = Color.random().hexColor

	jDict = {'color1': c, 'color2': d}
	return json.dumps(jDict)

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

