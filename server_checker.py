from flask import Flask, request, abort
from hashlib import sha1
from api import MessageType

app = Flask(__name__)

token = 'zmarsarc'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if signature_checked(request.args):
            return request.args['echostr']
    elif request.method == 'POST':
        meg_typ = get_meg_type(request.data)
        info = meg_typ(request.data)
        info.from_user_name, info.to_user_name = info.to_user_name, info.from_user_name
        return str(info.dump())
    abort(500)

def get_meg_type(data):
    from xml.etree.ElementTree import ElementTree
    tree = ElementTree(data)
    t = tree.find('MsgType').text
    if t == 'test':
        return MessageType.text
    if t == 'image':
        return MessageType.image
    if t == 'voice':
        return MessageType.voice
    if t == 'video':
        return MessageType.video
    if t == 'shortvideo':
        return MessageType.shortvideo
    if t == 'location':
        return MessageType.location
    if t == 'link':
        return MessageType.link

def signature_checked(args):
    sorted_args = sorted([token, args['timestamp'], args['nonce']])
    local_signature = sha1(''.join(sorted_args)).hexdigest()
    return args['signature'] == local_signature

if __name__ == '__main__':
    app.run(port=8000)
