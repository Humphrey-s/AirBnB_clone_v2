#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, render_template
from models import *
from models import storage
from models.state import State, City
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<uuid:id>', strict_slashes=False)
def states(id=None):
    """display a HTML page:"""
    states = storage.all(State).values()
    return render_template('9-states.html', states=states, id=id)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
