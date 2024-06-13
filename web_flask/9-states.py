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
def states():
    """display a HTML page:"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def get_state(id=None):
    """display a HTML page:"""
    states = storage.all(State).values()
    specific_state = storage.get(State, id)
    print(specific_state)
    return render_template(
                '9-states.html',
                states=states,
                specific_state=specific_state)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
