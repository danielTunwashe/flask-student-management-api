#To Create our user table we first import our db instance from utils
from ..utils import db 
from datetime import datetime

#Then, we create our databse table via classes
class RegisteredStudentCoursesGrade(db.Model):
#first define the table name
    __tablename__='registeredStudentCoursesGrades'
    id=db.Column(db.Integer(),primary_key=True)
    grade=db.Column(db.String(5),nullable=False)
    score=db.Column(db.Integer(),nullable=False)
    course_name=db.Column(db.String(30),nullable=False)
    course_id=db.Column(db.Integer(),nullable=False)
    course_unit=db.Column(db.Integer(),nullable=False)
    date_registered = db.Column(db.DateTime(), default=datetime.utcnow)
    #Relationship between student table and registeredStudentCourseGrades table
    student=db.Column(db.Integer(),db.ForeignKey('students.id'))
    
    
    #Special function to return a string representation of these objects
    def __repr__(self):
        return f"<RegisteredStudentCoursesGrade {self.id}>"
    
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