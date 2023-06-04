import unittest
from flask import Flask
from flask.testing import FlaskClient

class MyFlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test Flask application
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

        # Create a test client
        self.client = self.app.test_client()

    def tearDown(self):
        # Clean up any resources after each test
        pass

    def test_hello_world(self):
        # Send a GET request to the '/' route
        response = self.client.get('/')

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response data is 'Hello, World!'
        self.assertEqual(response.data.decode(), 'Hello, World!')

    def test_custom_route(self):
        # Send a GET request to a custom route
        response = self.client.get('/custom')

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response data contains 'Custom Route'
        self.assertIn('Custom Route', response.data.decode())

if __name__ == '__main__':
    unittest.main()
