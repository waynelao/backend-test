"""
Index index (main) view.

URLs include:
/
"""
import flask
import index
from index.model import get_db
import copy




@index.app.route('/', methods=["GET"])
def show_index():
    # construct the context dictionary
    context = {}
    context['results'] = []
    # get the country and title
    country = ''
    type1 = ''
    type2 = ''
    if 'country' in flask.request.args:
        country = flask.request.args['country']
    if 'movie' in flask.request.args:
        type1 = flask.request.args['movie']
    if 'tvshow' in flask.request.args:
        type2 = flask.request.args['tvshow']
    context['country'] = country
    context['type1'] = type1
    context['type2'] = type2

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
        context['results'].append(copy.deepcopy(showDict))
        index += 1
        if index > 5:
            break
    
    return flask.render_template("index.html", **context)