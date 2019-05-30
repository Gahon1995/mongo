from service.user_service import UserService
from test.test_base import TestBase
from utils.func import pretty_models
from web.app import app, api_rules


class TestFlask(TestBase):

    def setup_class(cls) -> None:
        super().setup_class()
        app.testing = True
        cls.client = app.test_client()
        cls.header = {'Content-Type': 'application/json'}
        api_rules()

    def test_login(self):
        response = self.client.post('/api/user/login', json={'username': 'admin', 'password': 'admin'})
        print(response.data)

    def test_users(self):
        response = self.client.get('/api/users')
        pretty_models(response.json['data']['list'], UserService.field_names)
        assert len(response.json['data']['list']) == 20
