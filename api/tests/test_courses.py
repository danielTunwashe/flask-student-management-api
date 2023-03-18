#importing the package for testing
import unittest
import json
#importing our create app function within from our main init.py
from .. import create_app
#import our config to use our confi_dict and set it to test case 
from ..config.config import config_dict
#Importing our db to access our database
from ..utils import db
#importing generate_password_hash from werkzeug 
from werkzeug.security import generate_password_hash
#Importing create access token from flask jwt to enable us to genereate an access token for the test
from flask_jwt_extended import create_access_token
from ..models.courses import Course



#creating test case class that comes from unittest
class StudentTestCaseClass(unittest.TestCase):
    #write a tear down and set up functions
    def setUp(self):
        #set up our app
        self.app=create_app(config=config_dict['test'])
        #create an app context and this app to our application context
        #create an app context
        self.appctx = self.app.app_context()
        #push current app to our app context
        self.appctx.push()
        
        #Create a test client which gives us the ability to test our API
        self.client=self.app.test_client()
        #create our database using the configuration, we defined in our config (import our db from the utils folder)
        db.create_all()
        
        
    
    #this destroy our database tables after it has been tested
    def tearDown(self):
        #destroy all our database
        db.drop_all()
        
        #pop the app context
        self.appctx.pop()
        #set our app to none
        self.app=None
        #Alsp, we set our client to none
        self.client=None
        
    
    def test_get_all_courses(self):
        
        '''
        Test Get all courses
        
        '''
        #Create a jwt for a dummy user since the route is protected
        
        #Create an access token for the test case (import create access token from flask_jwt_extended)
        token = create_access_token(identity='test')
        
        #Also indicate the Authorization headers and Bearer identity
        headers={
            "Authorization":f"Bearer {token}"
        }
        
        response=self.client.get('/course/get-all',headers=headers)
        
        #Check if the test returns a 200 status code which is ok and it is expected that it returns an empty list because there is nothing in the database
        assert response.status_code == 200
        
        #check if the test returns an empty list as exepected
        assert response.json == []       

        
        
    def test_api_register_course(self):
        response = self.client.post('/course/add', json={
            'course_name': 'testcourse',
            'course_instructor': 'testinstructor',
            'course_unit': 5,
            'no_of_student_to_be_enrolled':10
        })
        assert response.status_code == 201

        # make sure the user is in the database
        course = Course.query.filter_by(course_name='testcourse').first()
        assert course is not None
        assert course.course_unit == 5
        
        
    def test_api_update_course_by_id(self):
        response = self.client.post('/course/add', json={
            'course_name': 'testcourse',
            'course_instructor': 'testinstructor',
            'course_unit': 5,
            'no_of_student_to_be_enrolled':10
        })
        
        
        response = self.client.put('/course/update/1', json={
            'course_name': 'testcourse1',
            'course_instructor': 'testinstructor',
            'course_unit': 6,
            'no_of_student_to_be_enrolled':10
        })
        assert response.status_code == 200

        # make sure the course is in the database
        course = Course.query.filter_by(course_name='testcourse1').first()
        assert course is not None
        assert course.course_unit == 6
        
    
    
    def test_api_get_specific_course_by_id(self):
        response = self.client.post('/course/add', json={
            'course_name': 'testcourse',
            'course_instructor': 'testinstructor',
            'course_unit': 5,
            'no_of_student_to_be_enrolled':10
        })
        
        
        response = self.client.get('/course/1', json={
            'course_name': 'testcourse',
            'course_instructor': 'testinstructor',
            'course_unit': 5,
            'no_of_student_to_be_enrolled':10
        })
        assert response.status_code == 200

        # make sure the course is in the database
        course = Course.query.filter_by(course_name='testcourse').first()
        assert course is not None
        assert course.course_unit == 5
    
    
    
    def test_api_delete_course_by_id(self):
        response = self.client.post('/course/add', json={
            'course_name': 'testcourse',
            'course_instructor': 'testinstructor',
            'course_unit': 5,
            'no_of_student_to_be_enrolled':10
        })
        
        
        response = self.client.delete('/course/delete/1', json={
            'course_name': 'testcourse',
            'course_instructor': 'testinstructor',
            'course_unit': 5,
            'no_of_student_to_be_enrolled':10
        })
        assert response.status_code == 204

        # make sure the course not is in the database
        course = Course.query.filter_by(course_name='testcourse1').first()
        assert course is None
        
    

        

            
        