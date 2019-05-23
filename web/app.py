from flask import Flask, render_template, request
from flask_cors import CORS

from main import init_connect
from service.user_service import UserService

app = Flask(__name__)
CORS(app)


def init_app():
    app.config['JSON_SORT_KEYS'] = False  # 使返回的字段不排序， 完成开发后可删除

    from web.api.user import UserGetUpdateDelete, UsersList
    app.add_url_rule('/users/<uid>/', view_func=UserGetUpdateDelete.as_view('user'))
    app.add_url_rule('/users/', view_func=UsersList.as_view('users'))

    app.run()


@app.route('/')
def index(is_login=False, user=None):
    if not is_login:
        return render_template('login.html')

    return render_template('index.html', user=user)


@app.route('/login.html', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')
    user = None
    if username and password:
        user = UserService().login(username, password)
    if user:
        print(user)
        print(user.to_dict())
        return index(True, user.to_dict())
    else:
        return render_template('login.html', message="登录失败")


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get_one('username')
#     password = request.form.get_one('password')
#     user = None
#     if username and password:
#         user = UserService.login(username, password)
#     if user:
#         return index(True, user)
#     else:
#         return render_template('login.html', message="登录失败")


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
    init_app()
