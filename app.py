import os
import requests
import random

from flask import Flask, request, jsonify

from transformations import transformations
from counting import yan_tan

API_TOKEN = os.environ.get('LTR_SLACK_API_TOKEN')
LOCAL_TOKEN = os.environ.get('LTR_LOCAL_TOKEN')
BOT_IGNORE_LIST = os.environ.get('BOT_IGNORE_LIST').split(',') \
    if 'BOT_IGNORE_LIST' in os.environ else []

app = Flask(__name__)


@app.route('/', methods=['POST'])
def respond():
    """
    Get a list of channel members and return an ordering
    """
    incoming_token = request.args.get("token", None)
    if not incoming_token or incoming_token != LOCAL_TOKEN:
        return ('', 404)

    channel_id = request.form['channel_id']
    command = request.form['command']
    text = request.form['text'].lower() if 'text' in request.form else 'random'
    if 'help' in text:
        return jsonify({
            "response_type": "in_channel",
            "text": "usage",
            "attachments": [
                {"text": f"{command} executed without arguments will present the scrum order, and with a 50% probability of applying a randomly chosen text transformation."},  # noqa
                {"text": f"{command} ({' | '.join(transformations.keys())})"},  # noqa
                {"text": f"{command} help (displays this message)"},
            ]
        })

    members_list = requests.post('https://slack.com/api/conversations.members',
                                 data={
                                     'token': API_TOKEN,
                                     'channel': channel_id,
                                 }).json()

    if not members_list['ok']:
        return "This is probably a private channel that I'm not invited to. Invite me if you want me to work here."  # noqa

    users = []
    for member in members_list['members']:
        name = requests.post('https://slack.com/api/users.info', data={
            'token': API_TOKEN,
            'user': member,
        }).json()
        if name['user']['real_name'] in BOT_IGNORE_LIST or not name['ok']:
            continue
        users.append(name['user']['real_name'].title())

    random.shuffle(users)

    if not text or 'random' in text or text == '':
        # rather than just randomly selecting between the transformations,
        # let make it only half-likely you'll get a transformation to make
        # it feel more special
        keys = list(transformations.keys())
        keys.remove('normal')
        text = random.choice(['normal', random.choice(keys)])
    try:
        order = [transformations[text](user) for user in users]
    except KeyError:
        return f"I don't understand '{text}', try 'help'."

    # differentiate duplicates, e.g. when the transformation only uses
    # first name and is deterministic.
    duplicates = []
    for k, v in enumerate(order):
        if v in order[0:k] + order[k+1:]:
            duplicates.append(k)
    for k in duplicates:
        order[k] += f' ({users[k]})'

    response = {
        "response_type": "in_channel",
        "text": "Scrum Order: ",
        "attachments":
            [{"text": "{}: {}".format(yan_tan(k),
                                      v)} for k, v in enumerate(order)]
    }

    return jsonify(response)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user
    # access support
    app.run(threaded=True, port=5000)
