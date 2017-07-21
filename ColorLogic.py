import random

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from colour import Color as Colour

# Color class, which holds a hex color and provides useful methods
class Color:

	@staticmethod
	def random():

		colString = "#%06x" % random.randint(0, 0xFFFFFF)
		return Color(colString)

	def __init__(self, hexColor):

		self.hexColor = hexColor
		self.colour = Colour(hexColor)

	def getColorVector(self):

		# Turns this color into a 5-dimensonal vector, for the model

		red = round(self.colour.red, 1)
		gre = round(self.colour.green, 1)
		blu = round(self.colour.blue, 1)
		sat = round(self.colour.saturation, 1)
		lum = round(self.colour.luminance, 1)

		return [red, gre, blu, sat, lum]

	def __repr__(self):

		return "Object of color {0}".format(self.hexColor)

# Model object! Uses the training data to make a random forest classifier, stored within
class Model: 

	# Specify parameters for each model here, used in creation
	def __init__(self, specificID):

		nEst = 24
		maxF = 8
		rounds = 10

		everyoneFile = "csv/everyone.csv"
		specificFile = "csv/" + specificID + ".csv"

		self.model = self.getModel(everyoneFile, specificFile, nEst, maxF, rounds)

	# Takes in all those parameters, returns the most accurate model trained by them
	def getModel(self, everyoneFile, specificFile, nEst, maxF, rounds):

		everyone = np.loadtxt(everyoneFile, delimiter = ',')
		trainData = [ row[:10] for row in everyone ]
		trainLabels = [ int(row[10]) for row in everyone ]

		userSpecific = np.loadtxt(specificFile, delimiter = ',')
		testData = [ row[:10] for row in userSpecific ]
		testLabels = [ int(row[10]) for row in userSpecific ]

		modelList = []

		# Here, we make 10 models, all based on the data from "everyone.csv"

		for i in range(rounds):

			model = RandomForestClassifier(n_estimators = nEst, max_features = maxF)
			model.fit(trainData, trainLabels)
			modelList.append(model)

		# Then, we sort them by which does best on the user-specific data, and take the best

		modelList.sort(key = lambda m : m.score(testData, testLabels))
		return modelList.pop()

	# Takes in a number of color pairs to get, returns that many "good" pairs via model
	def getLikedPairs(self, numToGet):

		assert self.model is not None, "Cannot get data from an empty model"

		colorsToGenerate = 200
		colorList = []
		vectorList = []

		# Generate colorsToGenerate different color pairs, add to list

		for i in range(colorsToGenerate):

			color1 = Color.random()
			color2 = Color.random()
			vector = color1.getColorVector() + color2.getColorVector()

			colorList.append([color1, color2])
			vectorList.append(vector)

		# Use the model to sort them by "most likely to be enjoyed by this user"

		predictions = self.model.predict_proba(vectorList)
		predictions = predictions[:, 1]
		order = np.argsort(predictions)
		pairsSorted = np.array(colorList)[order]

		return pairsSorted[-numToGet:]








