import pytest, logging, hashlib
from app import app, cache
from blueprints import db
from blueprints.user.model import Users
from flask import Flask, request, json

def reset_db():
    db.drop_all()
    db.create_all()
    newUser = Users('al7262', 'azzahra@lamuri.com', 'Alt3rr4')
    db.session.add(newUser)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(internal=False):
    if internal:
        cachename = 'test-internal-token'
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
    else:
        cachename = 'test-token'
        data = {
            'username': 'al7262',
            'password': 'Alt3rr4'
        }
    token = cache.get(cachename)
    if token is not None:
        return token
    req = call_client(request)
    res = req.get('/auth', query_string=data)
    resjson = json.loads(res.data)
    logging.warning('RESULT: %s', resjson)
    assert res.status_code==200
    cache.set(cachename, resjson['token'], timeout=60)
    return resjson['token']