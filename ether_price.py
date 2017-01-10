from flask import Flask
from flask_ask import Ask, statement
import json, requests
import logging

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.intent('GetEtherPriceIntent')
def get_ether_price():
    url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD'
    ether_price = json.loads(requests.get(url=url).text)
    rtn = "1 Ether currently costs " + str(ether_price["BTC"]) + " bitcoin and " + str(ether_price["USD"]) + " <say-as interpret-as='spell-out'>US</say-as> dollars"
    return statement(rtn)


@ask.intent('GetEtherPrice')
def get_price():
    get_ether_price()


@ask.intent('LaunchRequest')
def launch_request():
    get_ether_price()


@ask.intent('AMAZON.HelpIntent')
def help():
    speechOutput = "I can tell you the price of ether in bitcoin and US dollars"
    reprompt = "How can I help you?"
    return statement(speechOutput).reprompt(reprompt)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye!")


@ask.intent('AMAZON.StopIntent')
def stop():
    cancel()


@ask.intent('SessionEndedRequest')
def end():
    cancel()


if __name__ == '__main__':
    app.run(debug=True)
