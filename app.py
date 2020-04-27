import os
import requests

from flask import Flask, request, jsonify
CHANNEL_NAME=os.environ.get('LTR_CHANNEL_NAME')
API_TOKEN=os.environ.get('LTR_SLACK_API_TOKEN')
LOCAL_TOKEN=os.environ.get('LTR_LOCAL_TOKEN')

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def respond():
    # Retrieve the name from url parameter
    incoming_token = request.args.get("token", None)


    # Check if user sent a name at all
    if not incoming_token or incoming_token != LOCAL_TOKEN:
        raise Exception("local key error")

    channels = requests.post('https://slack.com/api/conversations.list', data={
        'token': API_TOKEN,
        'types': 'private_channel'
    }).json()['channels']

    for channel in channels:
        if channel['name'] == CHANNEL_NAME:
            channel_id = channel['id']

    members = requests.post('https://slack.com/api/conversations.members', data={
        'token': API_TOKEN,
        'channel': channel_id,
    }).json()['members']


    users = []
    for member in members:
        users.append(requests.post('https://slack.com/api/users.info', data={
            'token': API_TOKEN,
            'user': member,
        }).json()['user']['real_name'])

    results = requests.post('https://slack.com/api/chat.postMessage', data={
        'token': API_TOKEN,
        'channel': CHANNEL_NAME,
        'text': ", ".join(users)
    })

    if results.response_code == 200:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "whoops"})

    return jsonify(dict(results))


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)