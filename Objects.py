import os
import random
from datetime import datetime

from colour import Color as Colour
from manage import db

class Response(db.Model):

	user = db.Column(db.Integer())
	stamp = db.Column(db.DateTime())

	hexCode1 = db.Column(db.String(8))
	hexCode2 = db.Column(db.String(8))
	opinion = db.Column(db.Integer())

	def __init__(self, user, hexCode1, hexCode2, opinion):

		self.user = user
		self.stamp = datetime.now()

		self.hexCode1 = hexCode1
		self.hexCode2 = hexCode2
		self.opinion = opinion

# Color class, which holds a hex color and provides useful methods
class Color:

	@staticmethod
	def random():

		colString = "#%06x" % random.randint(0, 0xFFFFFF)
		return Color(colString)

	def __init__(self, hexColor):

		self.hexColor = hexColor
		self.colour = Colour(hexColor)

	def colorVec(self):

		# Turns this color into a 5-dimensonal vector, for the model

		red = round(self.colour.red, 1)
		gre = round(self.colour.green, 1)
		blu = round(self.colour.blue, 1)
		sat = round(self.colour.saturation, 1)
		lum = round(self.colour.luminance, 1)

		return [red, gre, blu, sat, lum]

	def __repr__(self):

		return "Object of color {0}".format(self.hexColor)



