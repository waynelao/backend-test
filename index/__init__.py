"""index package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (index/config.py)
app.config.from_object('index.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable INDEX_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export INDEX_SETTINGS=secret_key_config.py
app.config.from_envvar('INDEX_SETTINGS', silent=True)


import index.api
import index.views
import index.model