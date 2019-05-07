from flask import Flask, render_template, request

from service.user_service import UserService

from main import init_connect

init_connect()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')
    success = False
    if username and password:
        success = UserService.login(username, password)
    if success:
        return 'welcome\n' + username + '\n' + password
    else:
        return render_template('login.html', message="登录失败")


if __name__ == '__main__':
    app.run()
