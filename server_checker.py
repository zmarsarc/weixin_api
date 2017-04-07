from flask import Flask, request, abort, render_template
from api import Access
from api import Config
from api import MessageType
from api.Utilties import signature_checked
import sqlite3
import os

app = Flask(__name__)

token = 'zmarsarc'


def connect_database():
    if not os.path.exists('userinfo.db'):
        ret = sqlite3.connect('userinfo.db')
        ret.executescript('schema.sql')
    else:
        ret = sqlite3.connect('userinfo.db')
    return ret

db = connect_database()


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


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if password_check(request.form['UserName'], request.form['Password'], db):
            return 'success'
        else:
            return 'deny'
    if request.method == 'GET':
        return render_template('admin_login.html')


@app.route('/admin/api/<name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def process_request(name):
    return name

if __name__ == '__main__':
    app.run(port=8000)


def password_check(username, password, db):
    result = db.execute("SELECT password FROM password WHERE username IS ?;", (username,))
    fetch = result.fetchone()
    return fetch == password
