import unittest
from .. import create_app
from ..utils import db
from ..config.config import config_dict
from flask_jwt_extended import create_access_token
from ..models.users import User, Admin

class TestAuth(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(config=config_dict['testing'])

        self.client = self.app.test_client()

        self.appctx = self.app.app_context()

        self.appctx.push()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_signup(self):
        # To register an admin

        admin_signup_data = {
            "name": "Testuser",
            "email": "admin@test.com",
            "user_type": "admin",
            "password": "password234"
        }
        admin_signup_response = self.client.post('/auth/signup', json=admin_signup_data)

        admin = User.query.filter_by(email=admin_signup_data['email']).first()

        assert admin.name == "Testuser"

        assert admin.email == admin_signup_data['email']

        assert admin_signup_response.status_code == 201




        # To register a student
        student_signup_data = {
            "name": "Student",
            "email": "student@test.com",
            "user_type": "student",
            "password": "password236"
        }

        student_signup_response = self.client.post('/auth/signup', json=student_signup_data)

        student = User.query.filter_by(email=student_signup_data['email']).first()

        assert student.name == "Student"

        assert student.email == student_signup_data['email']

        assert student_signup_response.status_code == 201




        # To sign in an Admin 
        admin_login_data = {
            "email": "admin@test.com",
            "password": "password234"
        }

        admin_login_response = self.client.post('/auth/login', json=admin_login_data)

        assert admin_login_response.status_code == 200

        token = create_access_token(identity=admin.id)

        headers = {
            'Authorization': f'Bearer {token}'
        }


        # To sign in a student 
        student_login_data = {
            "email": 'student@test.com',
            "password": "password236"
        }

        student_login_response = self.client.post('/auth/login', json=student_login_data)

        assert student_login_response.status_code == 200

        token = create_access_token(identity=student.id)

        headers = {
            'Authorization': f'Bearer {token}'
        }



        
        #To activate a test admin
        admin_activate_data = {
            "name": "Admin",
            "email": "admin@aotem.com",
            "user_type": "admin",
            "password": "password",
            "id": '2'

        }

        admin_activate_response = self.client.post('/auth/signup', json=admin_activate_data)

        admin = Admin.query.filter_by(email=admin_activate_data['email']).first()

        token1 = create_access_token(identity=admin)

        headers = {
            'Authorization': f'Bearer {token1}'
        }
