from flask_restx import Namespace,Resource,fields
from ..models.users import Admin,Student,User
from ..models.courses import Course,Score,StudentCourse
from http import HTTPStatus
from flask import request
from ..utils import db,letter__to_gpa_grade,grade
from flask_jwt_extended import jwt_required
from ..decorators import teacher_required,admin_required,admin_or_teacher_required,student_required

student_namespace=Namespace('students', description='a namespace for students')


student_model =student_namespace.model (
    'StudentGetCreate',{
    'id': fields.String(),
    'name': fields.String(required=True, description="the name of the Student"),
    'username': fields.String(required=False, description='the username of the Student'),
    'email': fields.String(required=True, description="the student's email address")
    

})

update_student_model=student_namespace.model (
    'GetUpdateDelete',{
    'name': fields.String(required=True, description="the name of the Student"),
    'email': fields.String(required=True, description="the email of the Student")
})


student_score_model = student_namespace.model (
    'StudentScore',{
    'student_id': fields.Integer(required=False, description='the ID of student'),
    'score': fields.Integer(required=True, description="the score value"),
}
)

course_model =student_namespace.model (
     'StudentCourseCreation',{
    'student_id': fields.String(required=True),
    # 'course_id':fields.String(required=True)
})

get_course_model =student_namespace.model (
    'StudentCoursesList',{
    'id': fields.Integer(),
    'name': fields.String(required=True, description="the course name"),
    'teacher_id': fields.Integer(),
    'course_code': fields.String(description="the course idss"),
    'created_at': fields.DateTime( description="the date of creating course"),
}

)
course_teacher_model = {
    'username': fields.String(required=True, description='username of the teacher'),
    'email': fields.String(required=True, description='email address of the teacher'),
    'name': fields.String(required=True, description="name of the teacher"),
    'staff_no': fields.String(required=True, description="course teacher ID"),
    'created_at': fields.DateTime( description="the date of creating course")
}

gpa_model = student_namespace.model(
    "GPA Model", {
        'name': fields.String(required=True, description="The Student Name"),
        'grade': fields.String(required=True, description="The Grade"),
        'gpa': fields.Float(required=True, description="The GPA")
        
    }
)




@student_namespace.route('/students/')
class StudentGetCreate(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Get all students"
    )
    @jwt_required
    def get (self):
       """
       get all students
       """
       students=Student.query_all()

       return students, HTTPStatus.OK
   



@student_namespace.route('/students/<int:student_id>')
class GetUpdateDelete(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='This allows the retrieval of a particular student by only admins and teachers',
        params={
            "student_id":"An id for a student"
        }
    )
    @admin_or_teacher_required()
    def get (self,student_id):
       """
       get student by id
       """
       student = Student.query.filter_by(id=student_id).first()
       if not student:
            return {'message':'Student does not exist'}, HTTPStatus.NOT_FOUND
       else:
        return student , HTTPStatus.OK

    @student_namespace.expect(update_student_model)    
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="update a student by ID",
        params={
            "student_id":"An id for a student"
        }
    )
    @admin_or_teacher_required()
    def put (self,student_id):
       """
       update a student by id
       """
       student = Student.query.filter_by(id=student_id).first()
       if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
       data = request.get_json()
       student.name = data.get('name')
       student.email = data.get('email')
       student.save()
       db.session.commit()
       return student, HTTPStatus.OK

    @student_namespace.expect(update_student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Delete a student by ID",
        params={
            "student_id":"An id for a student"
        }
    )
    @admin_required()
    def delete(self,student_id):
       """
       delete a student by id
       """
       student = Student.query.filter_by(id=student_id).first()
       if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
       student.delete()
       return {'message': 'Student deleted successfully'}, HTTPStatus.OK




#course

@student_namespace.route('')
class StudentCoursesList(Resource):
    @student_namespace.marshal_with(get_course_model)
    @student_namespace.doc(
        description="Retrieves all student courses",
        params={
            "student_id":"An id for a student",
            
        }
    )
    @admin_or_teacher_required()
    def get(self):
        """
        Retrieve all student courses
        """  
        courses = Course.query.all()

        return courses, HTTPStatus.OK   

        # student = Student.query.filter_by(id=student_id).first()
        # if not student:
        #     return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        
        # student_course = StudentCourse.get_courses_by_student_id(student_id)
        # return student_course, HTTPStatus.OK


@student_namespace.route('/<int:course_id>')
class GetStudentCourses(Resource):
    @student_namespace.marshal_with(get_course_model)
    @student_namespace.doc(
        description="Get a student course by ID",
        params={
            "course_id":"An id for a student",
            
        }
        
    )
    @admin_or_teacher_required()
    def get(self, course_id):
        """
            Get a student course by ID
        """
        course = Course.get_by_id(course_id)
        if not course:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        else:
            return course, HTTPStatus.OK
        
    

@student_namespace.route('')
class CreateStudentCourse(Resource):
    @student_namespace.expect(course_model)
    @student_namespace.doc(
        description="Register a student for a course",
        params={
            "student_id":"An id for a student",
            "course_id":"An id for a student course"
        }
    )
    @teacher_required()
    @jwt_required()
    def post(self, course_id):
        """
            Register a Student for a course 
        """
        
        data = request.get_json()
        student_id = data.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {
                'message': "Student or Course not found"
            }, HTTPStatus.NOT_FOUND
        
        if student:
            student_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if student_course:
                return {
                    'message': "{} has already registered for this course".format(student.name)
                }, HTTPStatus.OK
            else:
                student_course = StudentCourse(student_id=student.id, course_id=course.id)
                student_course.save()
                return {
                    'message': "{} registered for the {} course successfully".format(student.name, course.name)
                }, HTTPStatus.CREATED
        



@student_namespace.route('/student/<int:student_id>/courses/grades')
class GetStudentCoursesGrades(Resource):

    @student_namespace.doc(
        description='This allows the retrieval of a particular student courses and grades by only admins and teachers'
    )
    @admin_or_teacher_required()
    def get(self, student_id):
        """
            Get all of a student's courses and grades by ID
        """


        
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        
        student_courses = StudentCourse.get_courses_by_student_id(student_id)
        if not student_courses:
            return {'message': 'Student not registered for any course'}, HTTPStatus.NOT_FOUND
        
        student_courses_grades = []
        for student_course in student_courses:
            course = Course.query.filter_by(id=student_course.id).first()
            score = Score.query.filter_by(student_id=student_id, course_id=student_course.id).first()
            if score:
                student_courses_grades.append({
                    'course_id': course.id,
                    'course_name': course.name,
                    'course_score': score.score,
                    'course_gpa': score.gpa,
                })
            else:
                student_courses_grades.append({
                    'course_id': course.id,
                    'course_name': course.name,
                    'course_score': 'Not yet graded',
                    'course_gpa': 'Not yet graded',
                })
        return student_courses_grades, HTTPStatus.OK




@student_namespace.route('/student/<int:student_id>/gpa')
class GetStudentGPA(Resource):
    @student_namespace.marshal_with(gpa_model)

    @teacher_required()
    def get(self, student_id,course_id):
        """
            Calculate a Student GPA
        """
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND
        
        if student:
            #To Calculate the gpa 
            student_courses = StudentCourse.get_courses_by_student_id(student_id)
            if not student_courses:
                return {'message': 'Student not registered for any course'}, HTTPStatus.NOT_FOUND
            
            score = Score.query.filter_by(student_id=student_id).first()
            grades = score.percent.split(",")
            gpa = sum(letter__to_gpa_grade(grade) for grade in grades) / len(grades)
            score.gpa = round(gpa, 2)
            db.session.commit()
            return score, HTTPStatus.OK