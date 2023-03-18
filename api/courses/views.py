#Creating our namespaces from flask_restx to access our Resources class which will be used as blueprints
from flask_restx import Resource,Namespace,fields
#importing our course class to create a new instance of our course
from ..models.courses import Course
#Importing HTTP status class
from http import HTTPStatus
#importing request from flask to access our data from the client
from flask import request
#importing sql-alchemy instance from utils
from ..utils import db
#Importing access token and refresh token to create a JWT Identity
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity



#Creating our namespace to seperate our application
course_namespace = Namespace('course',description="A namespace for course")


#Createing a module for serialization (import fields from flask_restx)
course_model=course_namespace.model(
    'Course',{
        'id':fields.Integer(description="An ID"),
        'course_name':fields.String(description="Name of course",required=True),
        'course_instructor':fields.String(description="Name of course instructor",required=True),
        'course_unit':fields.Integer(description="Unit of course",required=True),
        'no_of_student_to_be_enrolled':fields.Integer(description="Total number of student that can be enrolled",required=True)
    }
)



#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@course_namespace.route('/add')
class addCourse(Resource):
    #First specify the data we are expecting or payload since we have created our serilization
    @course_namespace.expect(course_model)
    #Return our object as json by marshaling it with our post_model
    @course_namespace.marshal_with(course_model)
    #Give our API a description
    @course_namespace.doc(
        description="Add a Course to the database"
    )
    def post(self):
        '''
        Add a course 
        
        '''
        #Access the data from our client through our course_namespace.payload (similar to request.getjson from flask)
        data = course_namespace.payload
        
        #Using the payload data which is a dictionary to create our post
        new_course=Course (
            course_name=data['course_name'],
            course_instructor=data['course_instructor'],
            course_unit=data['course_unit'],
            no_of_student_to_be_enrolled=data['no_of_student_to_be_enrolled']
        )
        
                
        #save our course to the database
        new_course.save()
        
        return new_course, HTTPStatus.CREATED
    

        
        

#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@course_namespace.route('/get-all')
class getAllCourse(Resource):
    #Want the object returned to be returned as json
    @course_namespace.marshal_with(course_model)
    #Protect our endpoint and since we want a new refresh token we have to set it to be True
    @jwt_required()
    #Give our API a description
    @course_namespace.doc(
        description="Get all Courses"
    )
    def get(self):
        '''
        Get all courses
        
        '''
        #First create a module that helps us serilaize the data we pass to our API as well as help us marshal our responses and then, our responses will be return as json 
        #Query all course from our database (import our course from models)
        course=Course.query.all()
        #Return all courses (return user returns all course as objects which is not json serializable) - (Import our HTTP status class from http)
        return course, HTTPStatus.OK
        

#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@course_namespace.route('/<int:course_id>')
class getSpecificCourse(Resource):
    #Make the object returned json serializable
    @course_namespace.marshal_with(course_model)
    #Give our API a description
    @course_namespace.doc(
        description="Get Specific Course by ID",
        params={
            "course_id":"An ID for getting a Specific Course"
        }
    )
    def get(self,course_id):
        '''
            Get a specific course by ID
        '''
        #Query for the course by its ID in the database
        course=Course.get_by_id(course_id)
        
        #Return our post and HTTP status
        return course,HTTPStatus.OK
    
    
    
        
#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@course_namespace.route('/update/<int:course_id>')
class updateCourse(Resource):
    #Make the object returned json serializable
    @course_namespace.marshal_with(course_model)
    #Return our response via flask restx and the module created
    @course_namespace.marshal_with(course_model)
    #Give our API a description
    @course_namespace.doc(
        description="Update a particular Course by ID",
        params={
            "course_id":"An ID for updating specific a course"
        }
    )
    def put(self,course_id):
        '''
            Update a course by ID
        '''
        #First get course ID
        course_to_update=Course.get_by_id(course_id)
        
        #Gets the data that comes from student as json
        data = request.get_json()
        
        #Update our user due to different data that comes from our json endpoint
        course_to_update.course_name=data.get('course_name')
        course_to_update.course_instructor=data.get('course_instructor')
        course_to_update.course_unit=data.get('course_unit')
        course_to_update.no_of_student_to_be_enrolled=data.get('no_of_student_to_be_enrolled')

        
        #Save to our database (import our sqlAlchemy instance from utils)
        db.session.add(course_to_update)
        db.session.commit()
        
        #return the updated student (we have to marshal with student_model) 
        return course_to_update, HTTPStatus.OK
    
        #Note content type must come before Authorization and bearer in insomia before updating 
        
        
        
        
#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@course_namespace.route('/delete/<int:course_id>')
class deleteCourse(Resource):
    #Make the object returned json serilizable
    @course_namespace.marshal_with(course_model)
    #Give our API a description
    @course_namespace.doc(
        description="Delete a Particular Course by ID",
        params={
            "course_id":"An ID for deleting a Specific Course"
        }
    )
    def delete(self,course_id):
        '''
            Delete a course by ID
        '''
        #query for course to delete
        course_to_delete=Course.get_by_id(course_id)
        
        #Use the simple method in the course model to delete easily
        course_to_delete.delete()
        
        #return a response
        return course_to_delete, HTTPStatus.NO_CONTENT
