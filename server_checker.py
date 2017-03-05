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
        info = MessageType.auto(request.data)
        info.from_user_name, info.to_user_name = info.to_user_name, info.from_user_name
        return str(info.dump())
    abort(500)

def signature_checked(args):
    sorted_args = sorted([token, args['timestamp'], args['nonce']])
    local_signature = sha1(''.join(sorted_args)).hexdigest()
    return args['signature'] == local_signature

if __name__ == '__main__':
    app.run(port=8000)
