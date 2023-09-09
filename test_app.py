
import json
import os

import unittest
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from database.models import Actor, Movie, db, db_drop_and_create_all


load_dotenv()


class castingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:postgres@localhost:5432', self.database_name)
        self.db = db

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        CASTINGASSISTANT = os.environ.get('ASSISTANT_TOKEN')
        CASTINGDIRECTOR = os.environ.get('DIRECTOR_TOKEN')
        CASTINGPRODUCER = os.environ.get('PRODUCER_TOKEN')
        self.casting_assistant_token = {
            'Authorization': 'Bearer {}'.format(CASTINGASSISTANT)}
        self.casting_director_token = {
            'Authorization': 'Bearer {}'.format(CASTINGDIRECTOR)}
        self.casting_producer_token = {
            'Authorization': 'Bearer {}'.format(CASTINGPRODUCER)}

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.drop_all()
            self.db.session.commit


# Testing actors endpoints

    def test_get_paginated_actors(self):
        res = self.client().get('/actors', headers=self.casting_director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/actors?page=1000', headers=self.casting_director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_delete_actor(self):
        # Add an actor first
        actor_data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male'
        }
        response = self.app.post('/actors', json=actor_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        actor_id = data['actor_id']

        # Delete the added actor
        response = self.app.delete(f'/actors/{actor_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], actor_id)

    def test_404_post_delete_actor(self):
        # Add an actor first
        actor_data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male'
        }
        response = self.app.post('/actors', json=actor_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        actor_id = data['actor_id']

        # Delete the added actor
        response = self.app.delete(f'/actors/{actor_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], actor_id)

        # Try to delete the same actor again (should fail)
        response = self.app.delete(f'/actors/{actor_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error'])

    def test_update_actor(self):
        # Add an actor first
        actor_data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male'
        }
        response = self.app.post('/actors', json=actor_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        actor_id = data['actor_id']

        # Update the actor
        updated_actor_data = {
            'name': 'Jane Doe',
            'age': 35,
            'gender': 'Female'
        }
        response = self.app.patch(
            f'/actors/{actor_id}', json=updated_actor_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], actor_id)

        # Retrieve the updated actor
        response = self.app.get(f'/actors/{actor_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Jane Doe')
        self.assertEqual(data['age'], 35)
        self.assertEqual(data['gender'], 'Female')

    def test_update_actor_error(self):
        # Add an actor first
        actor_data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male'
        }
        response = self.app.post('/actors', json=actor_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        actor_id = data['actor_id']

        # Update the actor with missing fields to simulate an error
        updated_actor_data = {
            'name': 'Jane Doe',
            'age': 35
        }
        response = self.app.patch(
            f'/actors/{actor_id}', json=updated_actor_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['error'], 'Missing field. Please provide all required fields.')

    # test movies endpoints

    def test_get_paginated_movies(self):
        res = self.client().get('/movies', headers=self.casting_director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/movies?page=1000', headers=self.casting_director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_delete_movie(self):
        # Add a movie first
        movie_data = {
            'title': 'The Matrix',
            'release_date': '1999-03-31'
        }
        response = self.app.post('/movies', json=movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        movie_id = data['movie_id']

        # Delete the added movie
        response = self.app.delete(f'/movies/{movie_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], movie_id)

    def test_404_post_delete_movie(self):
        # Add a movie first
        movie_data = {
            'title': 'The Matrix',
            'release_date': '1999-03-31'
        }
        response = self.app.post('/movies', json=movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        movie_id = data['movie_id']

        # Delete the added movie
        response = self.app.delete(f'/movies/{movie_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], movie_id)

    def test_update_movie(self):
        # Add a movie first
        movie_data = {
            'title': 'The Matrix',
            'release_date': '1999-03-31'
        }
        response = self.app.post('/movies', json=movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        movie_id = data['movie_id']

        # Update the movie
        updated_movie_data = {
            'title': 'The Matrix Reloaded',
            'release_date': '2003-03-31'
        }
        response = self.app.patch(
            f'/movies/{movie_id}', json=updated_movie_data)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movie_error(self):
        # Add a movie first
        movie_data = {
            'title': 'The Matrix',
            'release_date': '1999-03-31'
        }
        response = self.app.post('/movies', json=movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])
        movie_id = data['movie_id']

        # Update the movie with missing fields to simulate an error
        updated_movie_data = {
            'title': 'The Matrix Reloaded'
        }
        response = self.app.patch(
            f'/movies/{movie_id}', json=updated_movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['error'], 'Missing field. Please provide all required fields.')

    # RBAC rols tests
    # Asstant
    def test_200_castingassistant_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_403_castingassistant_role_post_actor(self):
        res = self.client().post('/actors', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
    # Director

    def test_200_castingdirector_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_403_castingdirector_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.casting_director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # Producer

    def test_200_castingproducer_post_movies(self):
        res = self.client().post('/movies', headers=self.casting_producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_401_castingproducer_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token is invalid.')


if __name__ == "__main__":
    unittest.main()
