#----------------------------------------------------------------------------#
# Imports and blueprint setup
#----------------------------------------------------------------------------#

import os, csv, json
from random import randint

from flask import Flask, Blueprint, render_template, request, make_response
from ColorLogic import Color, Model

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

colorApp = Blueprint('colorApp', __name__,
	template_folder = 'templates', static_folder = 'static')

#----------------------------------------------------------------------------#
# Basic views -- Displaying choice screen or results, with data
#----------------------------------------------------------------------------#

@colorApp.route('/')
def home():

	sessionID = request.cookies.get('session')
	if sessionID is None: sessionID = str(randint(0, 100000))

	c = Color.random().hexColor
	d = Color.random().hexColor

	resp = make_response(render_template('main.html', color1 = c, color2 = d))
	resp.set_cookie('session', sessionID)

	return resp

@colorApp.route('/results/<sessionID>')
def results(sessionID):

	model = Model(sessionID)
	colorPairs = model.getLikedPairs(3)

	hexPairs = [[pair[0].hexColor, pair[1].hexColor] for pair in colorPairs]

	return render_template('results.html', pairs = hexPairs)

#----------------------------------------------------------------------------#
# The big one -- called by AJAX to add a new training color pair
#----------------------------------------------------------------------------#

@colorApp.route('/handleResponse')
def handler():

	returned1 = Color(request.args.get("color1"))
	returned2 = Color(request.args.get("color2"))
	response = int(request.args.get("response"))

	sessionID = request.cookies.get('session')

	# We add both the vectors (c1, c2) and (c2, c1) so we get double the training

	row = returned1.getColorVector() + returned2.getColorVector() + [response]
	backwards = returned2.getColorVector() + returned1.getColorVector() + [response]

	with open('csv/everyone.csv', 'a') as everyone:

		writer = csv.writer(everyone, delimiter = ',')
		writer.writerow(row)
		writer.writerow(backwards)

	# Write to both an "everyone" CSV for training, and a user-specific file

	with open('csv/' + sessionID + '.csv', 'a') as specific:

		writer = csv.writer(specific, delimiter = ',')
		writer.writerow(row)
		writer.writerow(backwards)

	# Then, just generate two new colors for them to classifyß

	c = Color.random().hexColor
	d = Color.random().hexColor

	jDict = {'color1': c, 'color2': d, 'sessionID': sessionID}
	return json.dumps(jDict)





