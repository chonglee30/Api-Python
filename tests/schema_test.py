import json
import requests
import pytest
from assertpy import assert_that, soft_assertions
from cerberus import Validator
from config import BASE_URI

article_schema = {
    'slug': {
        'type': 'string',
        'required': True
    },
    'title': {
        'type': 'string',
        'required': True
    },
    'description': {
        'type': 'string',
        'required': True
    },
    'body': {
        'type': 'string',
        'required': True
    },
    'tagList': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'string'
        }
    },
    'createdAt': {
        'type': 'string',
        'required': True
    },
    'updatedAt': {
        'type': 'string',
        'required': True
    },
    'favorited': {
        'type': 'boolean',
        'required': True
    },
    'favoritesCount': {
        'type': 'integer',
        'required': True
    },
    'author': {
        'type': 'dict',
        'required': True,
        'schema': {
            'username': {
                'type': 'string',
                'required': True
            },
            'bio': {
                'nullable': True
            },
            'image': {
                'type': 'string',
                'required': True
            },
            'following': {
                'type': 'boolean',
                'required': True
            }
        }
    }
}

articles_response_schema = {
    'articles': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': article_schema
        }
    },
    'articlesCount': {
        'type': 'integer',
        'required': True
    }
}

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
    responseBody = response.json()
    token = responseBody["user"]["token"]
    return token

def test_read_article_expected_schema(token):
    response = get_all_articles(token)
    response_data = response.json()
    validator = Validator(articles_response_schema)
    with soft_assertions():
        is_valid = validator.validate(response_data)
        assert_that(is_valid).is_true()
        assert_that(validator.errors).is_empty()

def test_read_all_articles_expected_schema(token):
    response = get_all_articles(token)
    response_data = response.json()
    articles = response_data['articles']
    validator = Validator(article_schema)
    with soft_assertions():
        for article in articles:
            is_valid = validator.validate(article)
            assert_that(is_valid).is_true()

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
    return response

