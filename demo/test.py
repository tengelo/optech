import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Hello, I am Alexas shophelper mode, how can I assist you today?'
    return question(speech_text).reprompt(speech_text).simple_card('Shophelper', speech_text)


@ask.intent('RestroomIntent')
def restroom():
    speech_text = 'The restroom is in the back'
    return statement(speech_text).simple_card('Restroom', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Ask me a question'
    return question(speech_text).reprompt(speech_text).simple_card('Help', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
