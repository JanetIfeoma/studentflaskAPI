from flask_restx import Namespace, Resource,fields
from flask import request
from ..models.users import User, Student,Admin
from werkzeug.security import check_password_hash,generate_password_hash
from http import HTTPStatus
from ..utils import db,generate_random_string
from werkzeug.exceptions import Conflict,BadRequest
from flask_jwt_extended import get_jwt_identity,create_access_token,create_refresh_token, jwt_required

auth_namespace=Namespace('auth', description='a namespace for authentication')

signup_model=auth_namespace.model(
    'SignUp',{
    'id':fields.Integer(),
    'username':fields.String(required=True, description='A username'),
    'email':fields.String(required=True, description='An email'),
    'password':fields.String(required=True, description='A password')


    }
)


user_model=auth_namespace.model(
    'User',{
    'id':fields.Integer(),
    'name':fields.String(required=True, description='A name'),
    'username':fields.String(required=True, description='A username'),
    'email':fields.String(required=True, description='An email'),
    'password_hash':fields.String(required=True, description='A password'),
    'is_admin':fields.Boolean(description=' this shows that the user is an admin')
    
    }
)


login_model=auth_namespace.model(
    'Login',{
    'email':fields.String(required=True, description='An email'),
    'password':fields.String(required=True, description='A password')

    }
)





@auth_namespace.route('/signup')
class SignUp(Resource):
    
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(
        description="""
            This endpoint is accessible to all user. 
            It allows the creation of an account as a student
            """
    )

    
    def post(self):
        """ Create a new student account """
        data = request.get_json()
        
        # Check if user already exists
       
        user = User.query.filter_by(email=data.get('email', None)).first()
        if user:
            return {'message': 'User already exists'} , HTTPStatus.CONFLICT
        
        # Create new user
        
        username=generate_random_string(12) 
       
        admission= 'STUDENTD@' +generate_random_string(6) 
        new_user =  Student(
            email=data.get('email'), 
            username=username,
            name=data.get('name'),
            user_type = 'student',
            password_hash = generate_password_hash(data.get('password')),
            )
        try:
            new_user.save()
        except:
            db.session.rollback()
            return {'message': 'An error occurred '}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'User has been registered successfully as{}'.format(new_user.user_type)}, HTTPStatus.CREATED


        

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.doc(
        description="""
            This endpoint is accessible to all users to login. 
            It allows tuser authentication
            """
    )
    @auth_namespace.expect(login_model)
    def post (self):
        """
        generate a jwt pair
        """
        
        data=request.get_json()

        email=data.get('email')
        password=data.get('password')

        user=User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash,password):
           access_token=create_access_token(identity=user.username)
           refresh_token=create_refresh_token(identity=user.username)

           response={
               'message': 'Login Successful',
               'access_token':access_token,
               'refresh_token':refresh_token
           }

           return response, HTTPStatus.OK
        
        raise BadRequest("Invalid Username or Password")
        





@auth_namespace.route('/refresh')
class Refresh(Resource):
    @auth_namespace.doc(
        description="""
            This is used by users to refresh their token
            It allows the user to generate a new access token
            """
    )

    @jwt_required(refresh=True)
    def post (self):
        """
        refresh a jwt pair
        """

        username=get_jwt_identity()

        access_token=create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK
