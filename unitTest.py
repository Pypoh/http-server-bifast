import unittest
import logging
from flask import Flask
from flask.testing import FlaskClient
from app import app


class HTTPServerUnitTest(unittest.TestCase):
    def setUp(self):
        # Create a test Flask application
        # app = Flask(__name__)
        app.config['TESTING'] = True

        logging.basicConfig(level=logging.DEBUG)
        self.logger = app.logger
        # Create a test client
        self.client = app.test_client()

    def tearDown(self):
        # Clean up any resources after each test
        pass

    def test_accountEnquiryOFI(self):
        response = self.client.post('/AccountEnquiryOFI')
        self.logger.debug(response.status_code)

        self.assertEqual(response.status_code, 200)

        # Get the response body
        response_body = response.data
        self.logger.debug(response_body)

if __name__ == '__main__':
    unittest.main()