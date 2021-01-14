from app import *
from models import *

from flask_testing import TestCase
import unittest
import requests
import json
import base64

from sqlalchemy.orm import close_all_sessions

class TestingUser(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        close_all_sessions()
        Base.metadata.create_all(engine)

    def tearDown(self):
        close_all_sessions()
        Base.metadata.drop_all(engine)

    def test_add_user_new(self):
        with app.test_client() as cl:
            user_data = {
                "username" : "first",
                "email" : "first@gmail.com",
                "password" : "first"
            }
            json_data= json.dumps(user_data).encode('utf-8')
            r1 = cl.open(path = '/music/user', method = 'POST',  headers={'Content-Type': 'application/json'})
            r2 = cl.open(path='/music/user', method='POST', data = json_data,headers={'Content-Type': 'application/json'})
            self.assertEqual(r1.status_code, 400)
            self.assertEqual(r2.status_code, 200)

    def test_delite_user(self):
        with app.test_client() as cl:
            user_data = {
                "username": "first",
                "email": "first@gmail.com",
                "password": "1111"
            }
            user_data2 = {
                "username": "second",
                "email": "second@gmail.com",
                "password": "2222"
            }
            json_data1 = json.dumps(user_data).encode('utf-8')
            json_data2 = json.dumps(user_data2).encode('utf-8')
            rr = cl.open(path='/music/user', method='POST', data = json_data1,headers={'Content-Type': 'application/json'})
            rr = cl.open(path='/music/user', method='POST', data=json_data2,headers={'Content-Type': 'application/json'})

            r2 = cl.open(path='/music/user/1', method='DELETE', headers={'Authorization': 'Basic ' + base64.b64encode('second@gmail.com:2222'.encode()).decode()})
            r1 = cl.open(path='/music/user/3', method='DELETE',headers={'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})

            r3 = cl.open(path='/music/user/1', method='DELETE', headers={'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})

            self.assertEqual(r2.status_code, 403)
            self.assertEqual(r1.status_code, 404)
            self.assertEqual(r3.status_code, 200)

class TestingPlaylist(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        close_all_sessions()
        Base.metadata.create_all(engine)
        cl = app.test_client()
        user_data1 = {
            "username": "first",
            "email": "first@gmail.com",
            "password": "1111"
        }
        user_data2 = {
            "username": "second",
            "email": "second@gmail.com",
            "password": "2222"
        }
        json_data1 = json.dumps(user_data1).encode('utf-8')
        json_data2 = json.dumps(user_data2).encode('utf-8')
        rr = cl.open(path='/music/user', method='POST', data=json_data1, headers={'Content-Type': 'application/json'})
        rr = cl.open(path='/music/user', method='POST', data=json_data2, headers={'Content-Type': 'application/json'})

    def tearDown(self):
        close_all_sessions()
        Base.metadata.drop_all(engine)

    def test_add_playlist(self):
        with app.test_client() as cl:
            musiclist_data1 = {
                "name" : "odin",
                "owner_id" : 1,
                "songs":["Du"],
                "status": "public"
            }
            musiclist_data2 = {
                "name": "dva",
                "owner_id": 2,
                "songs": ["Du", "ca"],
                "string": "private"
            }
            json_data1 = json.dumps(musiclist_data1).encode('utf-8')
            json_data2 = json.dumps(musiclist_data2).encode('utf-8')
            r1 = cl.open(path = '/music/playlist', method = 'POST', data = json_data1 ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})

            r2 = cl.open(path = '/music/playlist', method = 'POST', data = json_data2 ,headers={'Content-Type': 'application/json'})
            self.assertEqual(r1.status_code, 200)
            self.assertEqual(r2.status_code, 400)

    def test_get_playlist(self):
        with app.test_client() as cl:
            musiclist_data1 = {
                "name": "odin",
                "owner_id": 1,
                "songs": ["Du"],
                "status": "public"
            }
            musiclist_data3 = {
                "name": "tri",
                "owner_id": 2 ,
                "songs": ["Du", "ca"],
                "status": "private"
            }

            json_data1 = json.dumps(musiclist_data1).encode('utf-8')
            json_data3 = json.dumps(musiclist_data3).encode('utf-8')

            r = cl.open(path = '/music/playlist', method = 'POST', data = json_data1 ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})
            r01 = cl.open(path = '/music/playlist', method = 'POST', data = json_data3 ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('second@gmail.com:2222'.encode()).decode()})

            r1 = cl.open(path = '/music/playlist/5', method = 'GET', headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})
            r2 = cl.open(path = '/music/playlist/1', method = 'GET', headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('second@gmail.com:2222'.encode()).decode()})
            r3 = cl.open(path = '/music/playlist/2', method = 'GET', headers={'Content-Type': 'application/json'})


            self.assertEqual(r1.status_code, 404)
            self.assertEqual(r2.status_code, 200)
            self.assertEqual(r3.status_code, 403)

    def test_delite_playlist(self):
        with app.test_client() as cl:
            musiclist_data1 = {
                "name": "odin",
                "owner_id": 1,
                "songs": ["Du"],
                "status": "public"
            }
            musiclist_data2 = {
                "name": "odin",
                "owner_id": 1,
                "songs": ["Du"],
                "status": "private"
            }
            json_data1 = json.dumps(musiclist_data1).encode('utf-8')
            json_data2 = json.dumps(musiclist_data2).encode('utf-8')

            r = cl.open(path = '/music/playlist', method = 'POST', data = json_data1 ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})
            r0 = cl.open(path = '/music/playlist', method = 'POST', data = json_data2 ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})


            r1 = cl.open(path = '/music/playlist/1', method = 'DELETE', headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})
            r3 = cl.open(path = '/music/playlist/2', method = 'DELETE', headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('second@gmail.com:2222'.encode()).decode()})
            r4 = cl.open(path = '/music/playlist/99', method = 'DELETE', headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('second@gmail.com:2222'.encode()).decode()})

            
            self.assertEqual(r1.status_code, 200)
            self.assertEqual(r3.status_code, 403)
            self.assertEqual(r4.status_code, 404)

    def test_put_playlist(self):
        with app.test_client() as cl:
            musiclist_data1 = {
                "name": "odin",
                "owner_id": 1,
                "songs": ["Du"],
                "status": "private"
            }
            json_data1 = json.dumps(musiclist_data1).encode('utf-8')
            r = cl.open(path = '/music/playlist', method = 'POST', data = json_data1 ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})

            new_playlist_data1 = {
                "name": "dva",
                "owner_id": 1,
                "songs": ["sec"],
                "status": "private"
            }
            json_data = json.dumps(new_playlist_data1).encode('utf-8')
            r1 = cl.open(path = '/music/playlist/1', method = 'PUT', data = json_data ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('second@gmail.com:2222'.encode()).decode()})
            r2 = cl.open(path = '/music/playlist/22', method = 'PUT', data = json_data ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})
            r3 = cl.open(path = '/music/playlist/1', method = 'PUT', data = json_data ,headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + base64.b64encode('first@gmail.com:1111'.encode()).decode()})

            self.assertEqual(r1.status_code, 403)
            self.assertEqual(r2.status_code, 400)
            self.assertEqual(r3.status_code, 200)

if __name__ == "__main__":
    unittest.main()