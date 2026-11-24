from json import dumps
import pytest
import requests
from assertpy import assert_that
from json import dumps
from utils.print_helpers import pretty_print

@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"

def test_read_all_users(base_url):
    response = requests.get(f"{base_url}/posts")
    #response = requests.get(BASE_URI)
    response_text = response.json()
    #pretty_print(response_text)
    assert response.status_code == 200
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    titles = [users['title'] for users in response_text]
    assert_that(titles).contains('non est facere')

def test_add_new_user(base_url):
    payload = dumps({
        "title": "Learning REST API",
        "body": "This is my first CRUD API test.",
        "userId": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(url=f"{base_url}/posts", data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(201)