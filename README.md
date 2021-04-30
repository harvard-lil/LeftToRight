# LeftToRight
Provides a suggested order for members of a channel doing a virtual standup. It grabs a list of members in the channel 
from which the slash command was called, and returns them in a randomized list, somtimes after having applied some fun
text transformations.


```
pip install -r requirements.txt
```

You'll need a slackbot with the following scopes/permissions added:
```
channels:read
chat:write
commands
users:read
```

In your environment (shell, etc.) you'll need these variables set:
```
export LTR_SLACK_API_TOKEN='xoxb-[etc.]' # your slack bot API token which slack uses to validate requests coming from your app
export LTR_LOCAL_TOKEN='somerandomsecret' # your locally set token which this app uses to validate requests coming from slack
```

You'll also need :
* to invite your bot to any private channel you'd want to use it from
* a slash command set up to point to the public URL of wherever you've got it deployed, plus your 
locally-set app token passed to the token argument. For example, if you had your token set to yay and 
app being served from http://deployed.wow/ltr/, this would yield a successful query:
``` http://deployed.wow/ltr/?token=yay```

In the command itself, you can specify a transformation by passing— 1337, shifted, or nicknames— or no transformation by
passing 'normal'. Without specifying, the command follows the default behavior or choosing a random transformation a
a little over half the time.

If you're doing development on this application, use [poetry](https://python-poetry.org/) to manage Python packages, but make sure to run

    poetry export -o requirements.txt

for deployment purposes, if there are any changes to `poetry.lock`.
