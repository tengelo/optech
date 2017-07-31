import logging
import os
import random

from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Hello, I am Alexas shophelper mode, how can I assist you today?'
	#session.attributes['question']=0
    return question(speech_text).reprompt(speech_text).simple_card('Shophelper', speech_text)


@ask.intent('RestroomIntent')
def restroom():
    speech_text = 'The restroom is in the back'
    return question(speech_text).simple_card('Restroom', speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Ask me a question. If you need an associate to help you then say call'
    return question(speech_text).reprompt(speech_text).simple_card('Help', speech_text)

@ask.intent('CallIntent')
def call():
	speech_text = 'Calling an associate'
	return statement(speech_text).simple_card('Calling',speech_text)

@ask.intent('ReturnIntent')
def returns():
	speech_text = 'You can return any item as long as you have the receipt'
	return question(speech_text).simple_card('Return Policy',speech_text)

@ask.intent('SizeIntent', mapping={'item':'Item', 'size': 'Size'})
def size(item,size):
	r=random.choice([True,False])
	if r:
		speech_text='Yes we do have a '+item+' in size '+size+'. Do you want me to call an associate to bring it to you?'
		session.attributes['question']=1
	else:
		speech_text='I am sorry we do not have '+item+' in size '+size+'. Do you want me to order it online for you?'
		session.attributes['question']=2
		session.attributes['item']=item
		session.attributes['size']=size
	return question(speech_text).reprompt(speech_text)
	
@ask.intent('YesIntent')
def yes():
	if session.attributes.get('question') is None or session.attributes.get('question')==0:
		speech_text='Ask me a question. If you need an associate to help you then say call'
	elif session.attributes.get('question')==1:
		speech_text='Calling an associate'
	elif session.attributes.get('question')==2:
		item=session.attributes.get('item')
		size=session.attributes.get('size')
		speech_text='Ordering a '+item+' in size '+size
	elif session.attributes.get('question')==3:
		speech_text='Ask me a question. If you need an associate to help you then say call'
	session.attributes['question']=0
	return question(speech_text).reprompt(speech_text)

@ask.intent('NoIntent')
def no():
	if session.attributes.get('question') is None or session.attributes.get('question')==0:
		speech_text='Ask me a question. If you need an associate to help you then say call'
		session.attributes['question']=0
	elif session.attributes.get('question')==1 or session.attributes.get('question')==2:
		speech_text='Is there anything else I can help you out with'
		session.attributes['question']=3
	elif session.attributes.get('question')==3:
		speech_text='Goodbye'
		return statement(speech_text)
	return question(speech_text).reprompt(speech_text)

@ask.intent('RewardIntent')
def reward():
	speech_text='For every dollar you spend, you earn one point. Every 150 points you earn, you will receive a coupon for $10 off your next purchase.' 
	return question(speech_text).simple_card('Rewards Program',speech_text)

@ask.intent('SaleIntent')
def sale():
	speech_text="There is currently a buy one get one free sale on jeans"
	return question(speech_text).simple_card('Sales',speech_text)

@ask.intent('PriceIntent')
def price():
	speech_text='Please scan the barcode'
	return question(speech_text).simple_card('Price',speech_text)

@ask.intent('AMAZON.CancelIntent')
def cancel():
	return statement("Goodbye")

@ask.intent('AMAZON.StopIntent')
def stop():
	return statement("Goodbye")

@ask.session_ended
def session_ended(): 
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
