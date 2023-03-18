import unittest
from .. import create_app
from ..utils import db
from ..config.config import config_dict
from werkzeug.security import generate_password_hash

class UnitTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(config=config_dict['testing'])

        self.appctx=self.app.app_context()

        self.appctx.push()

        self.client=self.app.test_client()

        db.create_all()


    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app=None
 
        self.client=None



    def test_user_signup(self):

        dataa={
            "name":"testyy",
            "username":"testyyuser",
            "email":"testyyuser@company.com",
            "password":"passwordtestyy234"
        }

        response=self.client.post('/auth/signup',json=dataa)    


        assert response.status_code==201