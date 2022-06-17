"""backend-test api server code."""
import flask
from flask import jsonify
import index
from index.model import get_db
import copy
import datetime
import pdb




@index.app.route('/api/v1/shows/', methods=['GET'])
def index_shows():
    """Return a list of shows from the country and the type"""
    country = flask.request.args.get('country').lower()
    # pdb.set_trace()
    type = ''
    sort = 'dateadded'

    if flask.request.args.get('type'):
        type = flask.request.args.get('type').lower()
    if flask.request.args.get('sort'):
        sort = flask.request.args.get('sort').lower()

    # construct the context dictionary
    context = {}
    context['shows'] = []

    # access the database
    cursor = get_db().cursor()

    # get the type, title, director, cast, country, rating, listed_in and description of the show
    # [{type:, title:, director:, cast:, country:, rating:, listed_in:, description:}]
    if not type and sort == 'dateadded':
        query = "SELECT * FROM netflixshows WHERE country = ? COLLATE NOCASE ORDER BY dateadded DESC;"
        dataShow = cursor.execute(query, (country,)).fetchall()
    elif not type and sort == 'releaseyear':
        query = "SELECT * FROM netflixshows WHERE country = ? COLLATE NOCASE ORDER BY releaseyear DESC;"
        dataShow = cursor.execute(query, (country,)).fetchall()
    elif type and sort == 'dateaded':
        query = "SELECT * FROM netflixshows WHERE type = ? COLLATE NOCASE AND country = ? COLLATE NOCASE ORDER BY dateadded DESC;"
        dataShow = cursor.execute(query, (type, country,)).fetchall()
    else:
        query = "SELECT * FROM netflixshows WHERE type = ? COLLATE NOCASE AND country = ? COLLATE NOCASE ORDER BY releaseyear DESC;"
        dataShow = cursor.execute(query, (type, country,)).fetchall()

    
    # pdb.set_trace()
    # get the show info
    index = 0
    for showDict in dataShow:
        context['shows'].append(copy.deepcopy(showDict))
        index += 1
        if index > 10:
            break

    return jsonify(**context)


@index.app.route('/api/v1/insertshows/', methods=['POST'])
def insert_shows():
    """Return a recently added show"""
    # construct the context dictionary
    context = {}
    # access the database
    cursor = get_db().cursor()

    # get the parameters (for demonstration, only support add
    # title and country now)
    title = flask.request.args.get('title')
    country = flask.request.args.get('country')
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # insert shows
    query = '''
            INSERT INTO netflixshows (
                type, title, director, 
                cast, country, dateadded,
                releaseyear, rating, 
                duration, listedin, 
                description) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
    cursor.execute(query, ("Movie", title, " ", " ", country,
                           date, 2022, " ", "100 min", " ", " "))
    get_db().commit()

    context['type'] = 'Movie'
    context['title'] = title
    context['country'] = country
    context['dateadded'] = date
    context['releaseyear'] = 2022
    context['duration'] = '100 min'
    return (jsonify(**context), 201)


@index.app.route('/api/v1/shows/<showid>/', methods=['DELETE'])
def delete_shows(showid):
    # construct the context dictionary
    context = {}
    # access the database
    cursor = get_db().cursor()

    # check is the show exists
    query = "SELECT * FROM netflixshows WHERE showid = ?;"
    dataShow = cursor.execute(query, (showid,)).fetchall()
    if not dataShow:
        raise InvalidUsage("Not Found", status_code=404)
    else:
        query = "DELETE FROM netflixshows WHERE showid = ?;"
        cursor.execute(query, (showid,))
        get_db().commit()
        return (jsonify(**context), 204)


@index.app.route('/api/v1/updateshows/', methods=['PATCH'])
def update_shows():
    # construct the context dictionary
    context = {}
    context['updated_shows'] = []
    # access the database
    cursor = get_db().cursor()
    # get the parameter for showid and description
    showid = flask.request.args.get('showid')
    description = flask.request.args.get('description').lower()

    # check is the show exists
    query = "SELECT * FROM netflixshows WHERE showid = ?;"
    dataShow = cursor.execute(query, (showid,)).fetchall()
    if not dataShow:
        raise InvalidUsage("Not Found", status_code=404)
    else:
        query = "UPDATE netflixshows SET description = ? WHERE showid = ?;"
        cursor.execute(query, (description, showid,))
        get_db().commit()
        query = "SELECT * FROM netflixshows WHERE showid = ?;"
        dataShow = cursor.execute(query, (showid,)).fetchall()
        context['updated_shows'].append(copy.deepcopy(dataShow))
        return (jsonify(**context), 202)


@index.app.route('/api/v1/', methods=['GET'])
def index_url():
    """Return a list of services available"""
    results = {
        "get and delete shows": "/api/v1/shows/",
        "insert shows": "/api/v1/insertshows/",
        "update shows": "/api/v1/updateshows/",
        "url": "/api/v1/",
    }
    return jsonify(**results)


class InvalidUsage(Exception):
    """For errors."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """For errors."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """For errors."""
        rvresult = dict(self.payload or ())
        rvresult['message'] = self.message
        rvresult['status_code'] = self.status_code
        return rvresult
