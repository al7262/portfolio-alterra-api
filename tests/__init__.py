import pytest, logging, hashlib
from app import app, cache
from blueprints import db
from blueprints.client.model import Clients
from blueprints.book.model import Books
from blueprints.user.model import Users
from flask import Flask, request, json

def reset_db():
    db.drop_all()
    db.create_all()
    secret = hashlib.md5('FIRST01'.encode()).hexdigest()
    client = Clients(key='NUMBER01', secret=secret, status=True)
    db.session.add(client)
    db.session.commit() 
    user = Users(name='Akira', age=26, sex='Male', client_id=1)
    db.session.add(user)
    db.session.commit() 
    book = Books(title='Book01', isbn='123-456-789', writer='Unknown')
    db.session.add(book)
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
            'client_key': 'internal',
            'client_secret': 'Int3rn4l$ecr3t'
        }
    else:
        cachename = 'test-token'
        data = {
            'client_key': 'NUMBER01',
            'client_secret': 'FIRST01'
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