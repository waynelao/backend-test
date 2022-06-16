"""backend-test api server code."""
import flask
from flask import jsonify
import index
from index.model import get_db
import copy
import pdb




@index.app.route('/api/v1/shows/', methods=['GET'])
def index_shows():
    """Return a list of shows from the country and the type"""
    country = flask.request.args.get('country').lower()
    # pdb.set_trace()
    type1 = ''
    type2 = ''
    if flask.request.args.get('movie'):
        type1 = flask.request.args.get('movie').lower()
    if flask.request.args.get('tvshow'):
        type2 = flask.request.args.get('tvshow').lower()

    # construct the context dictionary
    context = {}
    context['shows'] = []

    # access the database
    cursor = get_db().cursor()

    # get the type, title, director, cast, country, rating, listed_in and description of the show
    # [{type:, title:, director:, cast:, country:, rating:, listed_in:, description:}]
    if type1 and not type2:
        # query = "SELECT * FROM netflixshows WHERE type = ? COLLATE NOCASE AND country = ? COLLATE NOCASE;"
        # dataShow = cursor.execute(query, (type1, country,)).fetchall()
        query = "SELECT * FROM netflixshows WHERE type = ? COLLATE NOCASE AND country = ? COLLATE NOCASE;"
        dataShow = cursor.execute(query, (type1, country,)).fetchall()
    elif not type1 and type2:
        query = "SELECT * FROM netflixshows WHERE type = ? COLLATE NOCASE AND country = ? COLLATE NOCASE;"
        dataShow = cursor.execute(query, (type2, country,)).fetchall()
    else:
        query = "SELECT * FROM netflixshows WHERE country = ? COLLATE NOCASE;"
        dataShow = cursor.execute(query, (country,)).fetchall()
    
    # pdb.set_trace()
    # get the show info
    index = 0
    for showDict in dataShow:
        context['shows'].append(copy.deepcopy(showDict))
        index += 1
        if index > 10:
            break

    return jsonify(**context)

    



@index.app.route('/api/v1/', methods=['GET'])
def index_url():
    """Return a list of services available"""
    results = {
        "shows": "/api/v1/shows/",
        "url": "/api/v1/",
    }
    return jsonify(**results)
