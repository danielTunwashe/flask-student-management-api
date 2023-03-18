#importing the package for testing
import unittest
#importing our create app function within from our main init.py
from .. import create_app
#import our config to use our confi_dict and set it to test case 
from ..config.config import config_dict
#Importing our db to access our database
from ..utils import db
#importing generate_password_hash from werkzeug 
from werkzeug.security import generate_password_hash
from ..models.students import Student
from flask_jwt_extended import create_access_token, create_refresh_token



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
        

    def test_student_registration(self):
        #Use our testclient from flask but first, we create our response variable
        data={
            "firstname":"test-firstname",
            "lastname":"test-lastname",
            "email":"test@gmail.com",
            #import generate_password_has from werkzeug.security
            "password": "password"
        }
        
        response=self.client.post('/student/sign-up',json=data)
        
        #check if student exists
        student=Student.query.filter_by(email="test@gmail.com").first()
        
        assert student.firstname == "test-firstname"
        
        #use the assert keyword to test
        assert response.status_code == 201
        
        #install pytest in order to run the test(pip install pytest)
        
        
    def test_login(self):
        
        data={
            "email":"test@gmail.com",
            #import generate_password_has from werkzeug.security
            "password": "password"
        }
        
        response=self.client.post('/student/login',json=data)
        
        #use the assert keyword to test (we use the status code of 400 in order to pass the test becasue we dont have any user created)
        assert response.status_code == 400
        
        
    def test_api_get_all_students(self):
        response = self.client.post('/student/sign-up', json={
            "firstname":"test-firstname",
            "lastname":"test-lastname",
            "email":"test@gmail.com",
            "password": "password"
        })
        
        
        response = self.client.get('/student/all-students')
        assert response.status_code == 200

        # make sure the student is in the database
        student = Student.query.filter_by(firstname='test-firstname').first()
        assert student is not None
        assert student.email == 'test@gmail.com'
    
    
        
        
    def test_api_update_a_student_by_id(self):
        response = self.client.post('/student/sign-up', json={
            "firstname":"test-firstname",
            "lastname":"test-lastname",
            "email":"test@gmail.com",
            "password": "password"
        })
        
        
        response = self.client.put('/student/update/1', json={
            "firstname":"test-firstname1",
            "lastname":"test-lastname",
            "email":"test1@gmail.com",
            "password": "password"
        })
        assert response.status_code == 200

        # make sure the student is in the database
        student = Student.query.filter_by(firstname='test-firstname1').first()
        assert student is not None
        assert student.email == 'test1@gmail.com'
        
     
     
        
    def test_api_delete_a_student_by_id(self):
        response = self.client.post('/student/sign-up', json={
            "firstname":"test-firstname",
            "lastname":"test-lastname",
            "email":"test@gmail.com",
            "password": "password"
        })
        
        
        response = self.client.delete('/student/delete/1', json={
            "firstname":"test-firstname",
            "lastname":"test-lastname",
            "email":"test@gmail.com",
            "password": "password"
        })
        assert response.status_code == 204

        # make sure the student is in the database
        student = Student.query.filter_by(firstname='test-firstname').first()
        assert student is None
        
        
        
    def test_api_generate_a_new_access_token(self):
        data_signup={
            "firstname":"test-firstname",
            "lastname":"test-lastname",
            "email":"test@gmail.com",
            "password": "password"
        }
        data_login={
            "email":"test@gmail.com",
            "password": "password"
        }
        response = self.client.post('/student/sign-up', json=data_signup)
        assert response.status_code == 201
        response=self.client.post('/student/login',json=data_login)
        assert response.status_code == 200
        refresh_token = create_refresh_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {refresh_token}"
        }
        response=self.client.post('/student/refresh',headers=headers)
        assert response.status_code == 200
        
        
       
        