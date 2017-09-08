import numpy as np
from sklearn.ensemble import RandomForestClassifier

from Objects import Response, Color

# Model object! Uses the training data to make a random forest classifier, stored within
class Model: 

	# Specify parameters for each model here, used in creation
	def __init__(self, specificID):

		allResponses = Response.query.all()
		userResponses = Response.query.filter(user = user)

		trainData, trainLabels = self.getDataAndLabels(allResponses)
		testData, testLabels = self.getDataAndLabels(userResponses)

		self.model = self.getModel(trainData, trainLabels, testData, testLabels)

	def getDataAndLabels(self, responses):

		forwards = lambda r: Color(r.hexCode1).colorVec() + Color(r.hexCode2).colorVec()
		backward = lambda r: Color(r.hexCode2).colorVec() + Color(r.hexCode1).colorVec()

		data = [ forwards(r) for r in responses ]
		labels = [ r.opinion for r in responses ]

		data += [ backward(r) for r in responses ]
		labels += [ r.opinion for r in responses ]

		return data, labels

	# Takes in all those parameters, returns the most accurate model trained by them
	def getModel(self, trainData, trainLabels, testData, testLabels):

		nEst = 24
		maxF = 8
		rounds = 10

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




