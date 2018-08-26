from unittest import TestCase, mock
from perfect_response import app
from flask import request, Response
import os

class TestPerfectResponse(TestCase):

    # Ensure all tests stay in testing mode
    def setUp(self):
        app.testing = True

    # Mock the environment variables in order to test slack validation
    @mock.patch.dict('os.environ', {'SLACK_VERIFICATION_TOKEN': 'mock_token'})
    @mock.patch.dict('os.environ', {'SLACK_TEAM_ID': 'mock_id'})
    def test_is_valid_perfect_response(self):
        # Mock the incoming slack request with the appropriate data needed for validation
        with app.test_request_context(data = {'token': 'mock_token', 'team_id': 'mock_id'}):
            # Set mocked get request
            incoming_token = request.form['token']
            incoming_id = request.form['team_id']
            # Set mocked environment
            environment_token = os.environ['SLACK_VERIFICATION_TOKEN']
            environment_id = os.environ['SLACK_TEAM_ID']
            # Assert that the mocked request and mocked environment are equal
            self.assertEqual(incoming_token, environment_token)
            self.assertTrue(incoming_id, environment_id)

            # Once validated, ensure a response is sent
            resp = Response(
                {
                    'response_type': 'in_channel',
                    'text': '<https://youtu.be/dQw4w9WgXcQ|Here is what you wanted!>'
                }
            )

            answer = app.process_response(resp)

            # Ensure response sent is valid
            self.assertTrue(answer)


    def test_perfect_response_without_validation(self):
        with app.test_client() as c:
            response = c.post('/perfect-response')

            self.assertEqual(response.status_code, 400)