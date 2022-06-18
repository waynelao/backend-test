"""Test for REST API."""
import pdb


def test_api_v1(client):
    '''sanity check for REST API'''
    response = client.get('/api/v1/')
    assert response.status_code == 200
    assert response.get_json() == {
        "get and delete shows": "/api/v1/shows/",
        "insert shows": "/api/v1/insertshows/",
        "update shows": "/api/v1/updateshows/",
        "url": "/api/v1/",
    }


def test_get_shows(client):
    '''Verify the GET endpoint'''
    # Verify the search function 
    response = client.get('/api/v1/shows/?country=United+States')
    assert response.status_code == 200
    
    # Verify the filter function
    response = client.get('/api/v1/shows/?country=china&type=tvshow')
    assert response.status_code == 200

    # Verify the sort function
    response = client.get('/api/v1/shows/?country=japan&type=movie&sort=releaseyear')
    assert response.status_code == 200

def test_post_shows(client):
    '''Verify the POST endpoint'''
    response = client.post('/api/v1/insertshows/?title=Master&country=Japan')
    pdb.set_trace()
    assert response.status_code == 201
    assert response.get_json()['type'] == 'Movie'
    assert response.get_json()['title'] == 'Master'
    assert response.get_json()['country'] == 'Japan'
    assert response.get_json()['releaseyear'] == 2022
    assert response.get_json()['duration'] == '100 min'


def test_delete_shows(client):
    '''Verify the DELETE endpoint'''
    # response = client.delete('/api/v1/shows/10000/')
    # assert response.status_code == 404

    response = client.delete('/api/v1/shows/200/')
    assert response.status_code == 204


def test_update_shows(client):
    '''Verify the PATCH endpoint'''
    response = client.patch('/api/v1/updateshows/?showid=200&description=nice+show')
    assert response.status_code == 202
    assert response.get_json()['description'].find('nice show') != -1

