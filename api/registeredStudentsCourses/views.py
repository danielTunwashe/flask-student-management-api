#Creating our namespaces from flask_restx to access our Resources class which will be used as blueprints
from flask_restx import Resource,Namespace,fields
#importing request from flask to access our data from the client
from flask import request
#importing our student class to create a new instance of our student
from ..models.students import Student
from ..models.courses import Course
from ..models.registeredStudentCourses import RegisteredStudentCourse
#Importing HTTP satus code from HTTP
from http import HTTPStatus
#Importing access token and refresh token to create a JWT Identity
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
#importing sql-alchemy instance from utils
from ..utils import db




#Creating our namespace to seperate our application
registered_students_course_namespace = Namespace('registerCourses',description="A namespace for registering student courses")



#Createing a module for serialization (import fields from flask_restx)
registeredStudentCourse_model=registered_students_course_namespace.model(
    'RegisteredStudentCourse',{
        'id':fields.Integer(description="An ID"),
        'semester':fields.String(description="Expecting a semster (First/Second)",required=True),
        'session_year':fields.String(description="Expecting a session/year (2016/2017 session)",required=True),
        'course_name':fields.String(description="Name of the course to be Registered",required=True),
        'course_id':fields.Integer(description="Course ID",required=True),
        'student':fields.Integer(description="Student ID")
    }
)


#Createing a module for serialization (import fields from flask_restx)
registeredStudentCourse_model2=registered_students_course_namespace.model(
    'RegisteredStudentCourse',{
        'id':fields.Integer(description="An ID"),
        'semester':fields.String(description="Expecting a semster (First/Second)",required=True),
        'session_year':fields.String(description="Expecting a session/year (2016/2017 session)",required=True),
        'course_name':fields.String(description="Name of the course to be Registered",required=True)
    }
)



#import resource class and create our class that inherits from our resource class
@registered_students_course_namespace.route('/add-new')
class registerCourses(Resource):
    #Protect our endpoint and since we want a new refresh token we have to set it to be True
    @jwt_required()
    #Decorator to help us expect the information in our serilizer in order to send data to our API
    @registered_students_course_namespace.expect(registeredStudentCourse_model)
    #Return our response via flask restx and the module created
    @registered_students_course_namespace.marshal_with(registeredStudentCourse_model)
    @registered_students_course_namespace.doc(
        description="Student Register For A Course"
    )
    def post(self):
        '''
            Register courses / add courses
        '''
        # results = db.session.query(Course).filter(Course.course_name=='Data-Structures and Algorithms'
        # for course in results:
        #     print(course.id)
        # return {"course_id":course.id}
        #Getting current student who registered a course ID
        
        email=get_jwt_identity()
        #Querying the student table to get the user username
        current_student=Student.query.filter_by(email=email).first()

        

        #Gets the data that comes from registeredStudentCourse as json so we return the ID of the course
        datastd = request.get_json()
        
        #Get the course name registered through our datastd and set course_id=0
        course_name=datastd.get('course_name') 
        course_id=0
        
        #Scan the database and check if the gotten course name exist and return the ID 
        results = db.session.query(Course).filter(Course.course_name==course_name)
        for course in results:
            course_id=course.id
        
        
        #Access the data from our student through our registered_students_course_namespace.payload (similar to request.getjson from flask)
        data = registered_students_course_namespace.payload
        
        #Using the payload data which is a dictionary to create our post
        new_registeredStudentCourse=RegisteredStudentCourse(
            semester=data['semester'],
            session_year=data['session_year'],
            course_name=data['course_name'],
            course_id=course_id
        )
        #specify the student who registered for the course (via the relationship between the student and the registeredStudentCourse table using the backref in our Student table) import get_jwt_identity
        new_registeredStudentCourse.studentCourse=current_student
 
        
        #save our post to the database
        new_registeredStudentCourse.save()
        
        return new_registeredStudentCourse, HTTPStatus.CREATED
        

#import resource class and create our class that inherits from our resource class
@registered_students_course_namespace.route('/get-all')
class getAllRegisteredCourses(Resource):
    #Want the object returned to be returned as json
    @registered_students_course_namespace.marshal_with(registeredStudentCourse_model)
    @registered_students_course_namespace.doc(
        description="Get/Retrieve all Registered Courses Added to the Database"
    )
    def get(self):
        '''
            Get all Registered courses 
        '''
        #First create a module that helps us serilaize the data we pass to our API as well as help us marshal our responses and then, our responses will be return as json 
        #Query all registered student course from our database (import our registeredStudentCourse from models)
        registeredStudentCourse=RegisteredStudentCourse.query.all()
        # for registeredCourses in registeredStudentCourse:
        #     print(registeredCourses.studentCourse.id)
        #Return all courses (return user returns all course as objects which is not json serializable) - (Import our HTTP status class from http)
        return registeredStudentCourse, HTTPStatus.OK


@registered_students_course_namespace.route('/registeredCourse/<int:registeredStudentCourse_id>')
class getSpecificRegisteredCourse(Resource):
    #Make the object returned json serializable
    @registered_students_course_namespace.marshal_with(registeredStudentCourse_model2)
    @registered_students_course_namespace.doc(
        description="Get Specific Registered Courses by ID",
        params={
            "registeredStudentCourse_id":"An ID for getting a Specific Registered Course"
        }
    )
    def get(self,registeredStudentCourse_id):
        '''
            Get a specific registered course by ID 
        '''
        #Query for the registeredStudentCourse by its ID in the database
        registeredStudentCourse=RegisteredStudentCourse.get_by_id(registeredStudentCourse_id)
        
        #Return our registeredStudentCourse and HTTP status
        return registeredStudentCourse,HTTPStatus.OK
    
    
    

@registered_students_course_namespace.route('/registeredCourse/all-students/<int:course_id>')
class getAllStudentsInAParticularCourse(Resource):
    #Make the object returned json serializable
    @registered_students_course_namespace.marshal_with(registeredStudentCourse_model)
    @registered_students_course_namespace.doc(
        description="Get/Retrieve all Students Registered In a Particular Course",
        params={
            "course_id":"An ID for getting all student registered in a particular course"
        }
    )
    def get(self,course_id):
        '''
            Get all students registered in a particular course
        '''
        #Filter the registeredStudentCourse database by the course_id and returns all  
        registeredStudentCourseAll=RegisteredStudentCourse.query.filter(RegisteredStudentCourse.course_id==course_id).all()
        
        #Return our registeredStudentCourse and HTTP status
        return registeredStudentCourseAll,HTTPStatus.OK
        
        
        
        

# @registered_students_course_namespace.route('/registeredCourse/student/<int:student_id>/course/<int:course_id>')
# class getAParticularStudentInAParticularCourse(Resource):
#     #Make the object returned json serializable
#     @registered_students_course_namespace.marshal_with(registeredStudentCourse_model)
#     def get(self,student_id,course_id):
#         '''
#             Get a particular student Registered in a particular Course
#         '''
#         reg = RegisteredStudentCourse.query.filter_by(student=student_id).all()
#         for re in reg:
#             registeredStudentCourseAll=RegisteredStudentCourse.query.filter(course_id==course_id  and re.student==student_id).first()
        
        
        
#         #Return our registeredStudentCourse and HTTP status
#         return registeredStudentCourseAll,HTTPStatus.OK





#import resource class and create our class that inherits from our resource class
@registered_students_course_namespace.route('/registeredCourse/update/<int:registeredStudentCourse_id>')
class updateRegisteredCourse(Resource):
    #Decorator to help us expect the information in our serilizer in order to send data to our API
    @registered_students_course_namespace.expect(registeredStudentCourse_model)
    #Return our response via flask restx and the module created
    @registered_students_course_namespace.marshal_with(registeredStudentCourse_model)
    @registered_students_course_namespace.doc(
        description="Update a Registered Student Course by ID",
        params={
            "registeredStudentCourse_id":"An ID for updating a Specific Registered Course"
        }
    )
    def put(self,registeredStudentCourse_id):
        '''
            Update Registed course by ID
        '''
        #First get registeredStudentCourse ID
        studentRegisteredCourse_to_update=RegisteredStudentCourse.get_by_id(registeredStudentCourse_id)
        
        #Gets the data that comes from studentRegisteredCourse_to_update as json
        data = request.get_json()
        
        #Get the course name registered through our datastd and set course_id=0
        course_name=data.get('course_name') 
        course_id=0
        
        #Scan the database and check if the gotten course name exist and return the ID 
        results = db.session.query(Course).filter(Course.course_name==course_name)
        for course in results:
            course_id=course.id
        
        #Update our user due to different data that comes from our json endpoint
        studentRegisteredCourse_to_update.semester=data.get('semester')
        studentRegisteredCourse_to_update.session_year=data.get('session_year')
        studentRegisteredCourse_to_update.course_name=data.get('course_name')
        studentRegisteredCourse_to_update.course_id=course_id

        #Save to our database (import our sqlAlchemy instance from utils)
        db.session.add(studentRegisteredCourse_to_update)
        db.session.commit()
        
        #return the updated student (we have to marshal with student_model) 
        return studentRegisteredCourse_to_update, HTTPStatus.OK
    
        
        
        

#import resource class and create our class that inherits from our resource class
@registered_students_course_namespace.route('/registeredCourse/delete/<int:registeredStudentCourse_id>')
class deleteRegisteredCourse(Resource):
    #Make the object returned json serilizable
    @registered_students_course_namespace.marshal_with(registeredStudentCourse_model)
    @registered_students_course_namespace.doc(
        description="Delete a Registered Student Course by ID",
        params={
            "registeredStudentCourse_id":"An ID for deleting a Specific Registered Course"
        }
    )
    def delete(self,registeredStudentCourse_id):
        '''
            Delete Registered course by ID
        '''
        #Query for the RegisteredStudentCourse to delete
        registeredStudentCourse_to_delete = RegisteredStudentCourse.get_by_id(registeredStudentCourse_id)
        
        #Use the simple method in the RegisteredStudentCourse model to delete easily
        registeredStudentCourse_to_delete.delete()
        
        #return a response
        return registeredStudentCourse_to_delete, HTTPStatus.NO_CONTENT