import pytest
import requests
from json import loads
from uuid import uuid4
from assertpy.assertpy import assert_that
from jsonpath_ng import jsonpath, parse
from config import BASE_URI
from utils.file_reader import read_file

@pytest.fixture(scope="module")
def token():
    userCredentials = {
        "email": 'vantest1@test.com',
        "password": 'Welcome#1'
    }
    payload = {
        "user": userCredentials
    }

    response = requests.post(f"{BASE_URI}/users/login", json = payload)
    assert response.status_code == 200
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    #return response.json()["user"]["token"]
    responseBody = response.json()
    token = responseBody["user"]["token"]
    print("TOKEN:", token)
    return token

@pytest.fixture(scope="module")
def create_data():
    payload = read_file('create_article.json')
    unique_title: str = f'FIFA {str(uuid4())}'
    payload['article']['title'] = unique_title
    yield payload

def test_article_creation(created_article, token):
    #create_article_with_unique_title(create_data, token)
    slug = created_article['article']['slug']
    print(slug)
    response = get_all_articles(token)
    articles = loads(response.text)['articles']
    jsonpath_expr = parse("$.[*].title")
    result = [match.value for match in jsonpath_expr.find(articles)]
    expected_title = created_article['article']['title']
    assert_that(result).contains(expected_title)

def test_delete_article(created_article, token):
    slug = created_article['article']['slug']
    print('delete article:')
    print(slug)
    headers = {
        'Authorization': f"Token {token}",
        'Accept': 'application/json'
    }
    response = requests.delete(f"{BASE_URI}/articles/{slug}", headers = headers)
    assert_that(response.status_code).is_equal_to(requests.codes.no_content)
    assert_that(response.status_code).is_equal_to(204)

@pytest.fixture(scope="module")
def created_article(create_data, token):
    return create_article_with_unique_title(create_data, token)

#@pytest.fixture(scope="module")
def create_article_with_unique_title(body:None, token):
    if body is None:
        unique_title: str = f'NFL {str(uuid4())}'
        payload = {
            'article': {
                'title': unique_title,
                'description': 'football',
                'body': 'football',
                'tagList': ['nfl']
            }
        }
    else:
        payload = body
    unique_article_title = body['article']['title']
    headers = {
        'Authorization': f"Token {token}",
        'Accept': 'application/json'
    }
    response = requests.post(f"{BASE_URI}/articles", json=payload, headers=headers)
    response_article = response.json()
    # print(response.status_code)
    # print(response.text)
    assert_that(response.status_code).is_equal_to(requests.codes.created)
    assert_that(response.status_code).is_equal_to(201)
    #return response.json() ['article'] #unique_title
    return response.json()

def get_all_articles(token):
    headers = {
        'Authorization': f"Token {token}",
        'Accept': 'application/json'
    }
    params = {
        'limit': 10,
        'offset': 0
    }
    response = requests.get(f"{BASE_URI}/articles", params=params, headers=headers)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response.status_code).is_equal_to(200)
    #return response.json()['articles']
    return response