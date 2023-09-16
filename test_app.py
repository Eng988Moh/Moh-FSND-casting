
import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from database.models import Actor, Movie, db, db_drop_and_create_all, setup_db


load_dotenv()


class castingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        # create and configure the app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = 'postgresql://postgres:0000@127.0.0.1:5432/{self.database_name}'
        self.db = db

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

        CASTINGASSISTANT = os.environ.get('CASTINGASSISTANT_TOKEN')
        CASTINGDIRECTOR = os.environ.get('CASTINGDIRECTOR_TOKEN')
        CASTINGPRODUCER = os.environ.get('CASTINGPRODUCER_TOKEN')
        self.casting_assistant_token = {
            'Authorization': 'Bearer {}'.format(CASTINGASSISTANT)}
        self.casting_director_token = {
            'Authorization': 'Bearer {}'.format(CASTINGDIRECTOR)}
        self.casting_producer_token = {
            'Authorization': 'Bearer {}'.format(CASTINGPRODUCER)}

    # def tearDown(self):
    #     """Executed after reach test"""
    #     with self.app.app_context():
    #         self.db.drop_all()
    #         self.db.session.commit


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
        with self.app.app_context():
            # Add an actor first
            actor_data = {
                'name': 'John Doe',
                'age': 30,
                'gender': 'Male'
            }
            actor = Actor(**actor_data)
            actor.insert()

            response = self.app.test_client().post(
                '/actors', headers=self.casting_producer_token, json=actor_data)
            data = json.loads(response.data)
            # print("Response:", response.status_code)
            # print("res:", data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['added'])
            actor_id = data.get('actor_id')
            # print("actor_id:", actor_id)

            # Delete the added actor
            response = self.app.test_client().delete(
                f'/actors/{actor_id}', headers=self.casting_producer_token)
            data = json.loads(response.data)
            # print("Responseeeeeeeeeeeeeeeee:", response.status_code)
            # print("resddddddddddddddd:", data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], True)

    def test_404_post_delete_actor(self):
        with self.app.app_context():
            # Add an actor first
            actor_data = {
                'name': 'John Doe',
                'age': 30,
                'gender': 'Male'
            }
            response = self.app.test_client().post(
                '/actors', json=actor_data, headers=self.casting_producer_token)
            data = json.loads(response.data)
            # print("Response:", response.status_code)
            # print("res:", data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['added'])
            actor_id = data.get('actor_id')

            # Delete the added actor
            response = self.app.test_client().delete(
                f'/actors/{actor_id}', headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], True)

            # Try to delete the same actor again (should fail)
            response = self.app.test_client().delete(
                f'/actors/{actor_id}', headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data['success'])
            self.assertIsNotNone(data['error'])

    # def test_update_actor(self):
    #     with self.app.app_context():
    #         # Add an actor first
    #         actor_data = {
    #             'name': 'John Doe',
    #             'age': 30,
    #             'gender': 'Male'
    #         }
    #         response = self.app.test_client().post(
    #             '/actors', json=actor_data, headers=self.casting_director_token)
    #         data = json.loads(response.data)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(data['success'])
    #         self.assertTrue(data['added'])
    #         actor_id = data['actor_id']

    #         updated_actor_data = {
    #             'name': 'Jane Doe',
    #             'age': 35,
    #             'gender': 'Female'
    #         }
    #         response = self.app.test_client().patch(
    #             f'/actors/{actor_id}', json=updated_actor_data, headers=self.casting_director_token)
    #         data = json.loads(response.data)
    #         print("Response1:", response.status_code)
    #         print("res1:", data)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(data['success'])
    #         self.assertEqual(data['updated'], True)

    #         # Retrieve the updated actor's information
    #         response = self.client().get(
    #             f'/actors/{actor_id}', headers=self.casting_assistant_token)
    #         data = json.loads(response.data)
    #         print("Response2:", response.status_code)
    #         print("res2:", data)

    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(data['success'], True)
    #         self.assertEqual(data['actor']['name'], 'Jane Doe')
    #         self.assertEqual(data['actor']['age'], 35)
    #         self.assertEqual(data['actor']['gender'], 'Female')

    def test_update_actor_error(self):
        with self.app.app_context():
            # Add an actor first
            actor_data = {
                'name': 'John Doe',
                'age': 30,
                'gender': 'Male'
            }
            response = self.app.test_client().post('/actors', json=actor_data,
                                                   headers=self.casting_director_token)
            data = json.loads(response.data)
            # print("Response:", response.status_code)
            # print("res:", data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['added'])
            actor_id = data['actor_id']

            # Update the actor with missing fields to simulate an error
            updated_actor_data = {
                'name': 'Jane Doe',
                'age': 35
            }
            response = self.app.test_client().patch(
                f'/actors/{actor_id}', json=updated_actor_data, headers=self.casting_director_token)
            data = json.loads(response.data)
            # print("Response:", response.status_code)
            # print("res:", data)
            self.assertEqual(response.status_code, 200)
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
        # print(data)
        # print(res.status_code)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_delete_movie(self):
        with self.app.app_context():
            # Add a movie first
            movie_data = {
                'title': 'The Matrix',
                'release_date': '1999-03-31'
            }
            response = self.app.test_client().post('/movies', json=movie_data,
                                                   headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['added'])
            movie_id = data['movie_id']

            # Delete the added movie
            response = self.app.test_client().delete(
                f'/movies/{movie_id}', headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['deleted'])

            # Try to delete the same movie again (should fail)
            response = self.app.test_client().delete(
                f'/movies/{movie_id}', headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data['success'])
            self.assertIsNotNone(data['error'])

    def test_404_post_delete_movie(self):
        with self.app.app_context():
            # Add a movie first
            movie_data = {
                'title': 'The Matrix',
                'release_date': '1999-03-31'
            }
            response = self.app.test_client().post('/movies', json=movie_data,
                                                   headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['added'])
            movie_id = data['movie_id']

            # Delete the added movie
            response = self.app.test_client().delete(
                f'/movies/{movie_id}', headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['deleted'])

            # Try to delete the same movie again (should fail)
            response = self.app.test_client().delete(
                f'/movies/{movie_id}', headers=self.casting_producer_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data['success'])
            self.assertIsNotNone(data['error'])

    # def test_update_movie(self):
    #     with self.app.app_context():
    #         # Add a movie first
    #         movie_data = {
    #             'title': 'The Matrix',
    #             'release_date': '1999-03-31'
    #         }
    #         response = self.app.test_client().post('/movies', json=movie_data,
    #                                                headers=self.casting_director_token)
    #         data = response.get_json()
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(data['success'])
    #         self.assertTrue(data['added'])
    #         movie_id = data['movie_id']

    #         # Update the movie
    #         updated_movie_data = {
    #             'title': 'The Matrix Reloaded',
    #             'release_date': '2003-03-31'
    #         }
    #         response = self.app.test_client().patch(
    #             f'/movies/{movie_id}', json=updated_movie_data, headers=self.casting_director_token)
    #         data = response.get_json()

    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(data['success'])

    #         # Retrieve the updated movie's information
    #         response = self.app.test_client().get(
    #             f'/movies/{movie_id}', headers=self.casting_director_token)
    #         data = response.get_json()

    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(data['success'], True)
    #         self.assertEqual(data['movie']['title'], 'The Matrix Reloaded')
    #         self.assertEqual(data['movie']['release_date'], '2003-03-31')

    def test_update_movie_error(self):
        with self.app.app_context():
            # Add a movie first
            movie_data = {
                'title': 'The Matrix',
                'release_date': '1999-03-31'
            }
            response = self.app.test_client().post('/movies', json=movie_data,
                                                   headers=self.casting_director_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['added'])
            movie_id = data['movie_id']

            # Update the movie with missing fields to simulate an error
            updated_movie_data = {
                'title': 'The Matrix Reloaded'
            }
            response = self.app.test_client().patch(
                f'/movies/{movie_id}', json=updated_movie_data, headers=self.casting_director_token)
            data = response.get_json()
            self.assertEqual(response.status_code, 422)
            self.assertFalse(data['success'])
            self.assertEqual(
                data['message'], 'Missing field. Please provide all required fields.')


if __name__ == '__main__':
    unittest.main()
