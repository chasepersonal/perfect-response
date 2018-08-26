import os
import logging
import dotenv

from flask import abort, Flask, jsonify, request

# Set up path to environment variable file
# Load variable information once path is set
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

# Initialize logger to set log messages
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Check to see that Slack request is valid
# Will check json token and team id against environment variables
def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


@app.route('/perfect-response', methods=['POST'])
def perfect_response():
    # If request is not valid, log a failure message then abort the request
    if not is_request_valid(request):
        logger.info('Verfication Token and Team ID requested do not match those on file locally')
        abort(400)

    # If request is valid, send back response type and text in json format
    return jsonify(
        {
            'response_type': 'in_channel',
            'text': '<https://youtu.be/dQw4w9WgXcQ|Here is what you wanted!>'
          }
    )

if __name__ == '__main__':
    app.run()