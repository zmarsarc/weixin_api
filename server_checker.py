from flask import Flask, request, abort, url_for
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


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '123456':
            return 'success'
        else:
            return 'deny'
    if request.method == 'GET':
        return url_for('static', filename='admin_login.html')

if __name__ == '__main__':
    app.run(port=8000)
