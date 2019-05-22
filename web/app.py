from flask import Flask, render_template, request

from main import init_connect
from service.user_service import UserService

app = Flask(__name__)


@app.route('/')
def index(is_login=False, user=None):
    if not is_login:
        return render_template('login.html')

    return render_template('index.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get_one('username')
    password = request.form.get_one('password')
    remember = request.form.get_one('remember')
    user = None
    if username and password:
        user = UserService.login(username, password)
    if user:
        return index(True, user)
    else:
        return render_template('login.html', message="登录失败")


@app.route('/admin')
def admin(is_login=False):
    if not is_login:
        return render_template('admin/login.html')
    pass


@app.route('/admin/login', methods=['post', 'get'])
def admin_login():
    username = request.form.get_one('username')
    password = request.form.get_one('password')
    success = False
    if username == 'admin' and password:
        success = UserService.login(username, password)
    if success:
        return 'welcome\n' + username + '\n' + password
    else:
        return render_template('admin/login.html', message="登录失败")
    pass


if __name__ == '__main__':
    init_connect()
    app.run()
