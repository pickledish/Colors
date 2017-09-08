#----------------------------------------------------------------------------#
# Imports and blueprint setup
#----------------------------------------------------------------------------#

import os, csv, json
from random import randint

from flask import Flask, Blueprint, render_template, request, make_response

from Objects import Response, Color
from Model import Model

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

	if sessionID is None: 
		sessionID = str(randint(0, 100000))

	c = Color.random().hexColor
	d = Color.random().hexColor

	resp = make_response(render_template('main.html', color1 = c, color2 = d))
	resp.set_cookie('session', sessionID)

	return resp

@colorApp.route('/results/<sessionID>')
def results(sessionID):

	model = Model(sessionID)
	colorPairs = model.getLikedPairs(3)

	hexPairs = [ [pair[0].hexColor, pair[1].hexColor] for pair in colorPairs ]

	return render_template('results.html', pairs = hexPairs)

#----------------------------------------------------------------------------#
# The big one -- called by AJAX to add a new training color pair
#----------------------------------------------------------------------------#

@colorApp.route('/handleResponse')
def handler():

	color1 = request.args.get("color1")
	color2 = request.args.get("color2")
	response = int(request.args.get("response"))
	sessionID = request.cookies.get('session')

	response = Response(sessionID, color1, color2, response)

	db.session.add(response)
	db.session.commit()

	# Then, just generate two new colors for them to classify

	c = Color.random().hexColor
	d = Color.random().hexColor

	jDict = {'color1': c, 'color2': d, 'sessionID': sessionID}
	return json.dumps(jDict)



