import pytest, logging
from . import app, cache, create_token, client, reset_db, call_client
from flask import Flask, request, json
import hashlib

class TestAuthCrud():
    def test_get_internal(client):
        req = call_client(request)
        data = {
            'client_key': 'internal',
            'client_secret': 'Int3rn4l$ecr3t'
        }
        res = req.get('/auth', query_string=data)
        assert res.status_code==200

    def test_get_normal(client):
        reset_db()
        req = call_client(request)
        data = {
            'client_key': 'NUMBER01',
            'client_secret': 'FIRST01'
        }
        res = req.get('/auth', query_string=data)
        assert res.status_code==200
    
    def test_get_invalid(client):
        reset_db()
        req = call_client(request)
        data = {
            'client_key': 'nnmnm',
            'client_secret': 'FIRST01'
        }
        res = req.get('/auth', query_string=data)
        assert res.status_code==401

    def test_post_internal(client):
        token = create_token(True)
        req = call_client(request)
        res = req.post('/auth', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code==200
    
    def test_post_normal(client):
        token = create_token()
        req = call_client(request)
        res = req.post('/auth', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code==200

    def test_refresh_internal(client):
        token = create_token(True)
        req = call_client(request)
        res = req.post('/auth/refresh', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code==200
    
    def test_refresh_normal(client):
        token = create_token()
        req = call_client(request)
        res = req.post('/auth/refresh', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code==200