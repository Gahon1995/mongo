from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from main import init_connect
from service.user_service import UserService
from utils.func import get_best_dbms_by_region
from utils.result import Result

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['JWT_SECRET_KEY'] = 'sfwertyad'
jwt = JWTManager(app)


def init_app():
    app.config['JSON_SORT_KEYS'] = False  # 使返回的字段不排序， 完成开发后可删除

    from web.api.user import UserGetUpdateDelete, UsersList
    app.add_url_rule('/users/<uid>/', view_func=UserGetUpdateDelete.as_view('user'))
    app.add_url_rule('/users/', view_func=UsersList.as_view('users'))

    app.run()


def get_jwt_user():
    info = get_jwt_identity()
    user = UserService().get_user_by_uid(uid=info['uid'], db_alias=get_best_dbms_by_region(info['region']))
    return user


@app.route('/protected')
@jwt_required
def protected():
    user = get_jwt_user()
    return '%s' % user


# @app.route('/')
# def index(is_login=False, user=None):
#     if not is_login:
#         return render_template('login.html')
#
#     return render_template('index.html', user=user)
#
#
# @app.route('/login.html', methods=['POST', 'GET'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')
#     remember = request.form.get('remember')
#     user = None
#     if username and password:
#         user = UserService().login(username, password)
#     if user:
#         print(user)
#         print(user.to_dict())
#         return index(True, user.to_dict())
#     else:
#         return render_template('login.html', message="登录失败")
#

@app.before_request
def cors():
    if request.method == 'OPTIONS':
        return


@app.route('/api/user/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username')
    password = request.json.get('password')
    user = None
    if username and password:
        user = UserService().login(username, password)
    if user:
        access_token = create_access_token(identity=user.to_dict(include=['uid', 'name', 'region']))
        return Result.gen_success({"token": access_token})
    else:
        return Result.gen_failed(404, "用户名或密码错误")
    # if user:
    #     return index(True, user)
    # else:
    #     return render_template('login.html', message="登录失败")


@app.route('/api/user/info', methods=['GET'])
@jwt_required
def info():
    user = get_jwt_user()
    user.avatar = "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
    info = user.to_dict()
    info['avatar'] = "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
    return Result.gen_success(info)
    pass


@app.route('/api/user/logout', methods=['GET', "POST"])
@jwt_required
def logout():
    # user = get_jwt_user()
    return Result.gen_success("")
    pass


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
