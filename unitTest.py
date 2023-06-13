import unittest
import logging
from flask import Flask
from flask.testing import FlaskClient

class HTTPServerUnitTest(unittest.TestCase):
    def setUp(self):
        # Create a test Flask application
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

        logging.basicConfig(level=logging.DEBUG)
        self.logger = self.app.logger
        # Create a test client
        self.client = self.app.test_client()

    def tearDown(self):
        # Clean up any resources after each test
        pass

    def test_accountEnquiryOFI(self):
        response = self.client.post('/AccountEnquiryOFI')
        self.logger.debug(response.location)

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
