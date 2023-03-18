#Creating our namespaces from flask_restx to access our Resources class which will be used as blueprints
from flask_restx import Resource,Namespace,fields
#importing request from flask to access our data from the client
from flask import request
#importing our user class to create a new instance of our student
from ..models.students import Student
#Importing pasword hash methods from werkzeug to has our password
from werkzeug.security import generate_password_hash,check_password_hash
#Importing HTTP satus code from HTTP
from http import HTTPStatus
#Importing access token and refresh token to create a JWT Identity
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
#importing sql-alchemy instance from utils
from ..utils import db
#Importing package from werkzeug to handle error that may arise from registering a student
from werkzeug.exceptions import Conflict, BadRequest




#Creating our namespace to seperate our application
student_namespace = Namespace('student',description="A namespace for student")


#Creating a serilization using flask restx and import (fields) from flask restx
signup_model=student_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'firstname':fields.String(required=True,description="Your First name"),
        'lastname':fields.String(required=True,description="A Last name"),
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password")
    }
    
)


#Another module that helps us get our student details after registration in a json format
student_model=student_namespace.model(
    'Student',{
        'id':fields.Integer(),
        'firstname':fields.String(required=True,description="A firstname"),
        'lastname':fields.String(required=True,description="A lastname"),
        'email':fields.String(required=True,description="An email"),
        'password_hash':fields.String(required=True,description="A password")
    }
)

#Creating serilization using flask restx for login module
login_model=student_namespace.model(
    'Login',{
        'email':fields.String(required=True,description="An emial"),
        'password':fields.String(required=True,description="A password")
    }
)



#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@student_namespace.route('/sign-up')
class signUpStudent(Resource):
    #Post because we are going to send request to the server
    #Decorator to help us expect the information in our serilizer in order to send data to our API
    @student_namespace.expect(signup_model)
    #Return our response via flask restx and the module created
    @student_namespace.marshal_with(student_model)
    #Give our API a description
    @student_namespace.doc(
        description="Student SignUp"
    )
    def post(self):
        '''
            Register / sign-up a student
        '''
        #Access the data from our client/student (import request from flask)
        data = request.get_json()
        
        #Trying to catch any error that may arise as a result of registering our student (from werkzeug.exceptions import conflict (409))
        try:
            #Create a new student by going to the user.py file to setup a function to perform that
            #create a new student instance (import our Student class from ..models.user)
            new_student=Student(
                firstname=data.get('firstname'),
                lastname=data.get('lastname'),
                email=data.get('email'),
                #Generate a password hash by importing from werkzeug built in flask
                password_hash= generate_password_hash(data.get('password' ))
                
                )
            #save new user to our database
            new_student.save()
            
            #return the newly created student via our signup module (after including marshal with at the top) then we just retun our HTTP status request
            #import HTTP status code from HTTP
            return new_student, HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(f"Student with {data.get('firstname')} and {data.get('email')} already exists")
        





#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@student_namespace.route('/login')
class loginStudent(Resource):
    #Decorator to help us expect the login_model information in our serilizer in order to send data to our API
    @student_namespace.expect(login_model)
    @student_namespace.doc(
        description="Student Login"
    )
    def post(self):
        '''
            Student Login after signing up and generating a JWT pair
        '''
        #Access the data from our client (import request from flask)
        data = request.get_json()
        #To login our user we first query to check if the student exist
        #first get our email and password
        email = data.get('email')
        password = data.get('password')
        #Scan the database and check if the student exist
        student=Student.query.filter_by(email=email).first()
        #check if user exist
        if (student is not None) and (check_password_hash(student.password_hash,password)):
            #Generate an access token with the identity of that current student (we need to import access token and refresh token from flask_jwt_extended)
            #create access token
            access_token=create_access_token(identity=student.email)
            #create refresh token
            refresh_token=create_refresh_token(identity=student.email)
            
            #return a dictionary containing an access token and a refresh token
            response={
                'access_token':access_token,
                'refresh_token':refresh_token
            }
            
            # return our response and status code
            return response, HTTPStatus.OK
        raise BadRequest("Invalid Email or Password")
        
#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@student_namespace.route('/all-students')
class getAllStudents(Resource):
    #Want the object returned to be returned as json
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Get/Retrieve all Students from the Database"
    )
    def get(self):
        '''
            Get/Retrieve all students
        '''
        #First create a module that helps us serilaize the data we pass to our API as well as help us marshal our responses and then, our responses will be return as json 
        #Query all students from our database (import our student from models)
        student=Student.query.all()
        #Return all users (return user returns all user as objects which is not json serializable) - (Import our HTTP status class from http)
        return student, HTTPStatus.OK

        
#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@student_namespace.route('/update/<int:student_id>')
class updateStudents(Resource):
    #Make the object returned json serializable
    @student_namespace.marshal_with(student_model)
    #Return our response via flask restx and the module created
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Update a Student by Student - ID",
        params={
            "student_id":"An ID for Updating a Student Data"
        }
    )
    def put(self,student_id):
        '''
            Update Students by ID
        '''
        #First get student ID
        student_to_update=Student.get_by_id(student_id)
        
        #Gets the data that comes from student as json
        data = request.get_json()
        
        #Update our user due to different data that comes from our json endpoint
        student_to_update.firstname=data.get('firstname')
        student_to_update.lastname=data.get('lastname')
        student_to_update.email=data.get('email')
        #student to update.password_hash is coming from the student database so we have to generate a new password because we are updating
        student_to_update.password_hash=generate_password_hash(data.get('password' ))
        
        #Save to our database (import our sqlAlchemy instance from utils)
        db.session.add(student_to_update)
        db.session.commit()
        
        #return the updated student (we have to marshal with student_model) 
        return student_to_update, HTTPStatus.OK
    
        #Note content type must come before Authorization and bearer in insomia before updating 

        

#import resource class and create our class that inherits from our resource class
#Defining our endpoints
@student_namespace.route('/delete/<int:student_id>')
class deleteStudents(Resource):
    #Make the object returned json serilizable
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Delete a Student by Student - ID",
        params={
            "student_id":"An ID for deleting a student data"
        }
    )
    def delete(self,student_id):
        '''
            Delete Students by ID
        '''
        #query for student to delete
        student_to_delete=Student.get_by_id(student_id)
        
        #Use the simple method in the student model to delete easily
        student_to_delete.delete()
        
        #return a response
        return student_to_delete, HTTPStatus.NO_CONTENT




#import resource class and create our class that inherits from our resource class
#Acquire a new access token when expired
@student_namespace.route('/refresh')
class Refresh(Resource):
    #Protect our endpoint and since we want a new refresh token we have to set it to be True
    @jwt_required(refresh=True)
    @student_namespace.doc(
        description="Generate a new access token after expiration"
    )
    def post(self):
        """
            Generate a new access token
        """
        #First, we need to get the identity of the current logged in student (ie we need to protect these route using JWT_Required and get_jwt_identity which will be imported from flask_jwt_extended)
        #Gets student identity using the token
        email=get_jwt_identity()
        
        #Create a new token based on the identity we have
        access_token=create_access_token(identity=email)
        
        #Return a response containing the new access token
        return {'access_token':access_token},HTTPStatus.OK
        
        # #returns the current user username with the access token
        # return {"username":username}
