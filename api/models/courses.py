from ..utils import db
from datetime import datetime
from ..models.users import Student


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    teacher_id= db.Column(db.Integer, db.ForeignKey('teachers.id'))
    students = db.relationship('Student')
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)
    student=db.Column(db.Integer() ,db.ForeignKey('students.id'))
   

    def __repr__(self):
        return f'{self.name}'

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


    def delete(self):
        db.session.delete(self)
        db.session.commit()


class StudentCourse(db.Model):
    __tablename__ = 'student_courses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)


    def __repr__(self) -> str:
        return f'{self.course_id}'
  
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_students_in_course_by(cls, course_id):
        students = Student.query\
            .join(StudentCourse, StudentCourse.student_id == Student.id)\
            .join(Course, Course.id == StudentCourse.course_id)\
            .filter(Course.id == course_id).all()

        return students
    
    @classmethod
    def get_courses_by_student_id(cls, student_id):
        courses = Course.query\
            .join(StudentCourse, StudentCourse.course_id == Course.id)\
            .join(Student, Student.id == StudentCourse.student_id)\
            .filter(Student.id == student_id).all()

        return courses




class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    score = db.Column(db.Float , nullable=False)
    grade = db.Column(db.String(5) , nullable=True )
    gpa = db.Column(db.Float)
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

    def __repr__(self):
        return f'{self.score}'
    
    def __init__(self, student_id, course_id, score ):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()    