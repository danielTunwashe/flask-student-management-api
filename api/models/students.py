#To Create our user table we first import our db instance from utils
from ..utils import db 
from datetime import datetime

#Then, we create our databse table via classes

class Student(db.Model):
#first define the table name
    __tablename__='students'
    id=db.Column(db.Integer(),primary_key=True)
    firstname=db.Column(db.String(50),nullable=False,unique=True)
    lastname=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False,unique=True)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    password_hash=db.Column(db.Text(),nullable=False)
    #Relationship between registeredStudentCourse table and student table
    registeredStudentCourse=db.relationship('RegisteredStudentCourse',backref='studentCourse',lazy=True)
    #Relationship between registeredStudentCoursesGrade table and student table
    registeredStudentCoursesGrade=db.relationship('RegisteredStudentCoursesGrade',backref='studentGrade',lazy=True)
    #Relationship between registeredStudentCoursesGradesGpa table and student table
    registeredStudentCoursesGradesGpa=db.relationship('RegisteredStudentCoursesGradesGpa',backref='studentGradeGpa',lazy=True)
    
    
    #Special function to return a string representation of these objects
    def __repr__(self):
        return f"<Student {self.firstname}>"
    
    #Special function to help us save our new user
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    #Special function to allow us query a specific user by its ID
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    #special function that allows one to delete a post
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    