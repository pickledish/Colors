import random

from sklearn.ensemble import RandomForestClassifier
from colour import Color as Colour
import numpy as np

class Color:

	@staticmethod
	def random():

		colString = "#%06x" % random.randint(0, 0xFFFFFF)
		return Color(colString)

	def __init__(self, hexColor):

		self.hexColor = hexColor
		self.colour = Colour(hexColor)

	def getColorVector(self):

		red = round(self.colour.red, 1)
		gre = round(self.colour.green, 1)
		blu = round(self.colour.blue, 1)
		sat = round(self.colour.saturation, 1)
		lum = round(self.colour.luminance, 1)

		return [red, gre, blu, sat, lum]

	def __repr__(self):

		return "Object of color {0}".format(self.hexColor)

class Model: 

	def __init__(self, specificID):

		nEst = 24
		maxF = 8
		rounds = 10

		everyoneFile = "csv/everyone.csv"
		specificFile = "csv/" + specificID + ".csv"

		self.model = self.getModel(everyoneFile, specificFile, nEst, maxF, rounds)

	def getModel(self, everyoneFile, specificFile, nEst, maxF, rounds):

		everyone = np.loadtxt(everyoneFile, delimiter = ',')
		trainData = [ row[:10] for row in everyone ]
		trainLabels = [ int(row[10]) for row in everyone ]

		userSpecific = np.loadtxt(specificFile, delimiter = ',')
		testData = [ row[:10] for row in userSpecific ]
		testLabels = [ int(row[10]) for row in userSpecific ]

		modelList = []

		for i in range(rounds):

			model = RandomForestClassifier(n_estimators = nEst, max_features = maxF)
			model.fit(trainData, trainLabels)
			modelList.append(model)

		modelList.sort(key = lambda m : m.score(testData, testLabels))
		return modelList.pop()

	def getLikedPairs(self, numToGet):

		assert self.model is not None, "Cannot get data from an empty model"

		colorsToGenerate = 200
		colorList = []
		vectorList = []

		for i in range(colorsToGenerate):

			color1 = Color.random()
			color2 = Color.random()
			vector = color1.getColorVector() + color2.getColorVector()

			colorList.append([color1, color2])
			vectorList.append(vector)

		predictions = self.model.predict_proba(vectorList)
		predictions = predictions[:, 1]
		order = np.argsort(predictions)
		pairsSorted = np.array(colorList)[order]

		return pairsSorted[-numToGet:]










