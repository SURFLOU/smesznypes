import os
import sys
import json
import random
from datetime import datetime

import requests
from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

def getRandomMessage(user_id, user_message):
    message = ["ciongaj zaslonke", "twoj stary zjezdza po tarce od sera", "twoj stary jest w darmowej rotacji championow w lolu", "twoj stary chowa sie za kratka w excelu recydywa", "twoj stary stoi mi pod oknem na akordenie gra", "twoj stary gej", "twoj stary wygral ksw zuli", "twoj stary zulitsu cwiczyl z zulem markiem", "twoj stary jezdzi tirem iveco lodowa jebana 99% damage", "twoj stary matizem napierdala 200", "twoj stary cie rucha w dymie monsunu", "twojemu staremu kanapki w szkole zabierali", "twoj stary ci kopa zasadzil w kolano to ci je wygial jak u bociana w druga strone", "twoj stary to ojcze doniz fujara stara", "twoj stary o godziny otwarcia twojej pizdy pytal", "twoj stary cie przylutowal do huja swojego", "twoj stary cie talerzami rzuca i mowi ze shurikenami napierdala"]
    messageA = "Jakie s\u0105 godziny pracy?"
    messageB = "Gdzie si\u0119 znajduje firma?"
    messageC = "Czy s\u0105 jakie\u015B promocje?"
    messageD = "Jakie potrawy serwujecie?"
    if(user_message == messageA or user_message == messageB or user_message == messageC or user_message == messageD):
        send_message(user_id, message[random.randint(0,(len(message)-1))])
    
                  
@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        getRandomMessage(user_id=sender_id, user_message=message_text)


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        msg = json.dumps(msg)
        print (u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
