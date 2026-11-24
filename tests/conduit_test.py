from json import dumps
import pytest
import requests
from assertpy.assertpy import assert_that, soft_assertions
from jsonpath_ng import jsonpath, parse
from json import dumps, loads
from uuid import uuid4
from config import BASE_URI
from utils.file_reader import read_file
from utils.print_helpers import pretty_print

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

def test_read_all_tags(token):
    print('Testing tags')
    print(token)
    response = requests.get(f"{BASE_URI}/tags",
            headers={"Authorization": f"Token {token}"})
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    response_tags = response.json();

    # 1. Verify 'tags' key exists and is a list
    assert "tags" in response_tags
    assert isinstance(response_tags["tags"], list)\

    # 2. Verify "Bondar Academy" exists anywhere in the tags array
    assert "Bondar Academy" in response_tags["tags"]

def test_new_article_created(create_new_article, token):
    #newly_created_article = create_new_article(token)
    #unique_title = newly_created_article['title']

    unique_title = create_new_article['title']
    articles = get_all_articles(token)
    assert_that(articles).extracting('title').is_not_empty().contains(unique_title)
    print (articles)
    is_new_article_created = search_created_article(articles, unique_title)
    print(is_new_article_created)
    #assert_that(is_new_article_created).is_equal_to(True)
    assert_that(is_new_article_created).is_not_empty()

def test_delete_article(create_new_article, token):
    slug = create_new_article['slug']
    headers = {
        'Authorization': f"Token {token}",
        'Accept': 'application/json'
    }
    response = requests.delete(f"{BASE_URI}/articles/{slug}", headers = headers)
    with soft_assertions():
        assert_that(response.status_code).is_equal_to(requests.codes.no_content)
        assert_that(response.status_code).is_equal_to(204)

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
    return response.json()['articles']

@pytest.fixture
def create_data():
    payload = read_file('create_article.json')
    unique_title: str = f'FIFA {str(uuid4())}'
    payload['title'] = unique_title
    yield payload



@pytest.fixture(scope="module")
def create_new_article(token):
    unique_title: str = f'NFL {str(uuid4())}'
    payload = {
        'article': {
            'title': unique_title,
            'description': 'football',
            'body': 'football',
            'tagList': ['nfl']
        }
    }
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
    return response.json() ['article'] #unique_title

def search_created_article(articles, title):
    return [article for article in articles if article['title'] == title]