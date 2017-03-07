import json

from flask import Blueprint
from flask import make_response
from flask import request

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from myconfig import channel_secret, channel_access_token

from urlapi import create

line = Blueprint('line', __name__)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@line.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)


    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        splitted = event.message.text.split()
        if splitted[0] == '/baru':
            response = baru(splitted)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

    return make_response('OK')

def baru(message):
    if len(message) == 1:
        return 'Penggunaan salah. Tulis "help" untuk bantuan.'

    url = message[1]
    if len(message) == 3:
        short = message[2]
    else:
        short = None

    response = create(local = True, url = url, short = short)
    if response['status']:
        return "URL pendek: {}".format(response['data']['url'])
    else:
        return "Ditemukan kesalahan: {}".format(response['data']['message'])
