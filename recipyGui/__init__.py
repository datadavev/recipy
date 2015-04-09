from flask import Flask, url_for
import os
from flask.ext.pymongo import PyMongo
from flask_bootstrap import Bootstrap
import re

recipyGui = Flask(__name__)
recipyGui.config['SECRET_KEY'] = 'geheim'

Bootstrap(recipyGui)

# Determines the destination of the build. Only usefull if you're using Frozen-Flask
recipyGui.config['FREEZER_DESTINATION'] = os.path.dirname(os.path.abspath(__file__))+'/../build'

# MongoDB settings
recipyGui.config['MONGO_DBNAME'] = 'recipyDB'

mongo = PyMongo(recipyGui)

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
recipyGui.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

def register_blueprints(app):
    # Prevents circular imports
    from recipyGui.views import runs
    recipyGui.register_blueprint(runs)

register_blueprints(recipyGui)

# Custom filters
@recipyGui.template_filter()
def highlight(text, query=None):
    """Filter to highlight query terms in search results."""
    if query:
        replacement = r'<mark>\1</mark>'
        for q in query.split(' '):
            text = re.sub(r'(?i)({})'.format(q), replacement, text)
    return text

recipyGui.jinja_env.filters['highlight'] = highlight
