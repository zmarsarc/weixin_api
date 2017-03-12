from flask import Flask, request, abort, render_template
from hashlib import sha1
from api import MessageType
from api import Access
from api import Config


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
            configer = Config.token('data/config.cfg')
            return Access.token(configer).value
        else:
            return 'deny'
    if request.method == 'GET':
        return render_template('admin_login.html')


@app.route('/admin/api/<name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def process_request(name):
    return name

if __name__ == '__main__':
    app.run(port=8000)
