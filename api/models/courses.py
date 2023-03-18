#To Create our user table we first import our db instance from utils
from ..utils import db 
from datetime import datetime

#Then, we create our databse table via classes

class Course(db.Model):
#first define the table name
    __tablename__='courses'
    id=db.Column(db.Integer(),primary_key=True)
    course_name=db.Column(db.String(50),nullable=False,unique=True)
    course_instructor=db.Column(db.String(50),nullable=False,unique=True)
    course_unit=db.Column(db.Integer(),nullable=False)
    no_of_student_to_be_enrolled=db.Column(db.Integer(),nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    
    #Special function to return a string representation of these objects
    def __repr__(self):
        return f"<Course {self.course_name}>"
    
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
    