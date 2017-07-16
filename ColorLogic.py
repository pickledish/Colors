from colour import Color as Colour
import numpy as np
import tensorflow as tf
import random
import shutil

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

def runModel():

	training_set = tf.contrib.learn.datasets.base.load_csv_without_header(filename = "eggs.csv", 
		target_dtype = np.int, features_dtype = np.float32, target_column = 10)

	testing_set = tf.contrib.learn.datasets.base.load_csv_without_header(filename = "test.csv", 
		target_dtype = np.int, features_dtype = np.float32, target_column = 10)

	feature_columns = [tf.contrib.layers.real_valued_column("", dimension = 10)]

	# ---------------------------------------------------------------------------

	def get_train_inputs():

		x = tf.constant(training_set.data)
		y = tf.constant(training_set.target)

		return x, y

	def get_test_inputs():
		x = tf.constant(testing_set.data)
		y = tf.constant(testing_set.target)

		return x, y

	# ---------------------------------------------------------------------------

	linOpt = tf.train.FtrlOptimizer(learning_rate = 0.10,
		l1_regularization_strength = 0.5, l2_regularization_strength = 2.0)

	dnnOpt = tf.train.AdagradOptimizer(learning_rate = 0.10, initial_accumulator_value = 0.1)

	# ---------------------------------------------------------------------------

	shutil.rmtree('colorModel', ignore_errors = True)

	classifier1 = tf.contrib.learn.LinearClassifier(feature_columns = feature_columns, model_dir = "colorModel",
		n_classes = 2, optimizer = linOpt)

	classifier1.fit(input_fn = get_train_inputs, steps = 2000)

	accuracy_score1 = classifier1.evaluate(input_fn = get_test_inputs, steps = 1)["accuracy"]
	print("\nTest Accuracy: {0:f}\n".format(accuracy_score1))

	# ---------------------------------------------------------------------------

	shutil.rmtree('colorModel', ignore_errors = True)

	classifier2 = tf.contrib.learn.DNNClassifier(feature_columns = feature_columns,
		hidden_units = [5], n_classes = 2, model_dir = "colorModel", optimizer = dnnOpt)

	classifier2.fit(input_fn = get_train_inputs, steps = 2000)

	accuracy_score2 = classifier2.evaluate(input_fn = get_test_inputs, steps = 1)["accuracy"]
	print("\nTest Accuracy: {0:f}\n".format(accuracy_score2))

	# ---------------------------------------------------------------------------

	shutil.rmtree('colorModel', ignore_errors = True)

	classifier3 = tf.contrib.learn.DNNLinearCombinedClassifier(n_classes = 2,
		linear_feature_columns=feature_columns, linear_optimizer=linOpt,
		dnn_feature_columns=feature_columns, dnn_hidden_units=[5], dnn_optimizer=dnnOpt)
	
	classifier3.fit(input_fn = get_train_inputs, steps = 2000)
	
	accuracy_score3 = classifier3.evaluate(input_fn = get_test_inputs, steps = 1)["accuracy"]
	print("\nTest Accuracy: {0:f}\n".format(accuracy_score3))

def runModel2():

	import optunity
	import optunity.metrics

	from sklearn.neighbors import KNeighborsClassifier
	from sklearn.svm import SVC
	from sklearn.naive_bayes import GaussianNB
	from sklearn.ensemble import RandomForestClassifier

	dataLoaded = np.loadtxt("eggs.csv", delimiter = ',')

	data = list()
	labels = list()

	for row in dataLoaded:
		data.append(row[:10])
		labels.append(int(row[10]))

	def train_svm(data, labels, kernel, C, gamma, degree, coef0):
		"""A generic SVM training function, with arguments based on the chosen kernel."""
		if kernel == 'linear':
			model = SVC(kernel=kernel, C=C)
		elif kernel == 'poly':
			model = SVC(kernel=kernel, C=C, degree=degree, coef0=coef0)
		elif kernel == 'rbf':
			model = SVC(kernel=kernel, C=C, gamma=gamma)
		else:
			raise ArgumentError("Unknown kernel function: %s" % kernel)
		model.fit(data, labels)
		return model

	@optunity.cross_validated(x=data, y=labels, num_folds=5)
	def performance(x_train, y_train, x_test, y_test,
					algorithm, n_neighbors=None, n_estimators=None, max_features=None,
					kernel=None, C=None, gamma=None, degree=None, coef0=None):
		
		if algorithm == 'k-nn':
			model = KNeighborsClassifier(n_neighbors=int(n_neighbors))
			model.fit(x_train, y_train)
		elif algorithm == 'SVM':
			model = train_svm(x_train, y_train, kernel, C, gamma, degree, coef0)
		elif algorithm == 'naive-bayes':
			model = GaussianNB()
			model.fit(x_train, y_train)
		elif algorithm == 'random-forest':
			model = RandomForestClassifier(n_estimators=int(n_estimators),
										   max_features=int(max_features))
			model.fit(x_train, y_train)
		else:
			raise ArgumentError('Unknown algorithm: %s' % algorithm)

		# predict the test set
		if algorithm == 'SVM':
			predictions = model.decision_function(x_test)
		else:
			predictions = model.predict_proba(x_test)[:, 1]

		x = optunity.metrics.roc_auc(y_test, predictions, positive=True)
		print(x)
		return x

	search = {'algorithm': {'k-nn': {'n_neighbors': [1, 5]},
						'SVM': {'kernel': {'linear': {'C': [0, 2]},
										   'rbf': {'gamma': [0, 1], 'C': [0, 10]},
										   'poly': {'degree': [2, 7], 'C': [0, 50], 'coef0': [0, 1]}
										   }
								},
						'naive-bayes': None,
						'random-forest': {'n_estimators': [10, 30],
										  'max_features': [5, 10]}
						}
		 }

	optimal_configuration, info, _ = optunity.maximize_structured(performance,
															  search_space=search,
															  num_evals=300)
	solution = dict([(k, v) for k, v in optimal_configuration.items() if v is not None])
	print('Solution\n========')
	print("\n".join(map(lambda x: "%s \t %s" % (x[0], str(x[1])), solution.items())))
	print(info.optimum)

def runModel3():

	from sklearn.ensemble import RandomForestClassifier
	import optunity.metrics

	trainLoaded = np.loadtxt("eggs.csv", delimiter = ',')
	testLoaded = np.loadtxt("test.csv", delimiter = ',')

	trainData = list()
	trainLabels = list()

	for row in trainLoaded:
		trainData.append(row[:10])
		trainLabels.append(int(row[10]))

	testData = list()
	testLabels = list()

	for row in testLoaded:
		testData.append(row[:10])
		testLabels.append(int(row[10]))

	nEst = 24
	maxF = 8

	model = RandomForestClassifier(n_estimators = nEst, max_features = maxF)
	model.fit(trainData, trainLabels)

	testy = Color("#a91d2e").getColorVector() + Color("#a448b1").getColorVector()

	predictions = model.predict_proba([testy])
	print(predictions)

	print(model.score(testData, testLabels))

if __name__ == "__main__":

	runModel3()












