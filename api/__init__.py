from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .student.views import student_namespace
from .config.config import config_dict
from .utils import db
from .models.courses import Course,StudentCourse,Score
from .models.users import User, Student,Admin,Teacher
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed


def create_app(config=config_dict['dev']):
    app=Flask(__name__)


    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    api=Api(app,
            version='1.0', 
            title='Student Management API', 
            description='A RestAPI for a Student Management service',
            authorizations=authorizations,
            security='apikey'
            )

    app.config.from_object(config)




    api.add_namespace(student_namespace)
    api.add_namespace(auth_namespace, path='/auth')
    db.init_app(app)
    
    jwt=JWTManager(app)

    migrate=Migrate(app,db)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error":"Method Not Allowed"}, 404
    

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error":"Not Found"}, 405

    

    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Admin':Admin,
            'Teacher':Teacher,
            'Student':Student,
            'Course':Course,
            'StudentCourse':StudentCourse,
            'Score':Score
        }




    return app