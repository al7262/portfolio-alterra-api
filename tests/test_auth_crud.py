import pytest, logging
from . import app, cache, create_token, client, reset_db, call_client
from flask import Flask, request, json
import hashlib

class TestAuthCrud():
    def test_get_admin(client):
        req = call_client(request)
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        res = req.get('/login', query_string=data)
        assert res.status_code==200

    def test_get_user(client):
        reset_db()
        req = call_client(request)
        data = {
            'username': 'al7262',
            'password': 'Alt3rr4'
        }
        res = req.get('/login', query_string=data)
        assert res.status_code==200