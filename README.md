# Colors

Answer 20 questions about which colors you think look good together, and train your own decision tree classifier to give you suggestions on new color pairings you'll probably like! Uses a very advanced Linux-Flask-CSV stack.

Whenever you answer whether you "like" a color pair or not, that pair is turned into a 10-dimensional feature vector (based on the red, green, blue, saturation, and lightness of both colors) and stored in an "everyone" CSV file and a specific-to-you CSV file. On clicking "See Similar", all vectors are loaded from both files and used to train a [random forest classifier](https://en.wikipedia.org/wiki/Random_forest) on the spot, which goes through a hundred or so random color-pair vectors and returns a few which it determines to be a "yes" with the highest probability. When I ran it myself with some of my own test data, it achieved an accuracy of 80% to 85% with a small training set, which is good enough for me.

I also took this opportunity to mess around with [Materialize.css](http://materializecss.com), because cards are nice and Google's material design needs to be sprayed in every place imaginable. It's a good library!

<hr>

### Tools Used

* [Materialize](http://materializecss.com), for the frontend framework
* [Flask](http://flask.pocoo.org/), for the backend framework
* [NumPy](http://www.numpy.org/), for some vector operations
* [SKLearn](http://scikit-learn.org/), for the random forest classifier

<hr>

### How to Run

The app is set up as a Flask blueprint, so assuming you have a Flask application set up, you can register it easily. Find the part of your project where you define the top-level Flask object, which is often `app = Flask(__name__)` and sometimes located in `manage.py`, if you have that file. Then, somewhere after that line, add:

```
from ColorApp import colorAppBlueprint
app.register_blueprint(colorAppBlueprint, url_prefix='/colors')
```