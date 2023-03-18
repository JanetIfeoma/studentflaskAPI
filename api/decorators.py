from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from .models.users import User
from functools import wraps
from http import HTTPStatus


def retrieve_user_type(ui:int):
    """
        Retrieve user type
        
        Args:
            ui (int): User id
    """

    user = User.query.filter_by(id=ui).first()

    if user:
        return user.user_type
    else:
        return None
    

def admin_required():
    """
        Admin required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if retrieve_user_type(claims['sub']) == 'admin':
                return fn(*args, **kwargs)
            return {
                'message': 'Admin access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def teacher_required():
    """
        Teacher required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt()
            print(user_id)
            if retrieve_user_type(user_id['sub']) == 'teacher':
                return fn(*args, **kwargs)
            return {
                'message': 'Teacher access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def student_required():
    """
        Student required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt()
            print(user_id)
            if retrieve_user_type(user_id['sub']) == 'student':
                return fn(*args, **kwargs)
            return {
                'message': 'Student access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def admin_or_teacher_required():
    """
        Admin or teacher required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt()
            print(user_id)
            if retrieve_user_type(user_id['sub']) == 'admin' or retrieve_user_type(user_id['sub']) == 'teacher':
                return fn(*args, **kwargs)
            return {
                'message': 'Admin or teacher access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper