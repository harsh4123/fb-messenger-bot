
import os
import sys
import json
from sultan.api import Sultan
import requests
from flask import Flask, request
import commands

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

a={}
@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
   # log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    bot_check(sender_id, message_text.lower())

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


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)

def bot_check(sender_id,message):

    if(hello(message)):
        m=hello(message)
    elif (what(message)):
        m=what(message)
    elif(cmd(message[0])):
        m=apply_command(message)
    elif("sultan"==cmd(message)):
        m=ls(message)
    elif(store(message)):
        m=store(message)
    elif(extract(message)):
        m=extract(message)
    elif(abuse(message)):
        m="fuck u don't abuse!!"
    else:
        m="shall i google it"
    send_message(sender_id,m)


def hello(message):
    hello=["hello","hi","hlo","hllo"]
    
    for i in hello :
        if i in message :
            return "hi , good to see u"
def what(message):
    what=['what','why','how','who','?']
    for i in what :
        if i in message :
                return "what do u mean  by "+message

def cmd(message):
    message=message.split(" ")[0]
    if("command"==message):
        return 1
    elif "sultan"==message:
        return message
def apply_command(message):
   return commands.getoutput(" ".join(message.split(" ")[1:]))

def ls(message):
    
    if("ls"==message[1]):
        with Sultan.load() as f:
            return " ".join(f.ls(message.split(" ")[2:]).run())
def store(message):
    message=message.split(" ")
    if(message[0]=="save"):
        a[message[1]]=message[2]
        return "info saved !!"
def extract(message):
    get=['get','extract','ask']
    info=['info','']
    for i in get:
        
    if i in message:
        if j in message:
        

def abuse(message):
    abuse=["fuck"]
    if

            


