from flask import Flask, render_template
from flask_ask import Ask, session, question, statement
import json, requests
import logging

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.intent('GetEtherPriceIntent')
def get_ether_price():
    url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD'
    ether_price = json.loads(requests.get(url=url).text)
    dollars, cents = ether_price["USD"] // 1, (100 * ether_price["USD"]) % 100
    rtn = "1 Ether currently costs " + str(ether_price["BTC"]) + " bitcoin and " + str(dollars) + " <say-as interpret-as='spell-out'>US</say-as> dollars and " + str(cents) + " cents"
    return statement(rtn)


@ask.launch
def launch_request():
    speechOutput = "I can tell you the price of ether in bitcoin and US dollars."
    reprompt = " How can I help you?"
    return question(speechOutput + reprompt)


@ask.intent('AMAZON.HelpIntent')
def help():
    speechOutput = "I can tell you the price of ether in bitcoin and US dollars."
    reprompt = " How can I help you?"
    return question(speechOutput + reprompt)


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Bye!")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Bye!")

@ask.session_ended
def session_ended():
    return statement("")


if __name__ == '__main__':
    app.run(debug=True)
