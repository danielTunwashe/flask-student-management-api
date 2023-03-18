#To Create our user table we first import our db instance from utils
from ..utils import db 
from datetime import datetime

#Then, we create our databse table via classes
class RegisteredStudentCoursesGradesGpa(db.Model):
#first define the table name
    __tablename__='registeredStudentCoursesGradesGpas'
    id=db.Column(db.Integer(),primary_key=True)
    gpa=db.Column(db.Float(),nullable=False)
    semester=db.Column(db.String(),nullable=False)
    session_year=db.Column(db.String(),nullable=False)
    #Relationship between student table and registeredStudentCourseGradesGpa table
    student=db.Column(db.Integer(),db.ForeignKey('students.id'))
    
    
    #Special function to return a string representation of these objects
    def __repr__(self):
        return f"<RegisteredStudentCoursesGradesGpa {self.id}>"
    
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