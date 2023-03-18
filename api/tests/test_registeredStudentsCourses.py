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
from ..models.registeredStudentCourses import RegisteredStudentCourse
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
        
        
    def test_api_student_register_courses_or_add_courses(self):
        data_student_add_course={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        }
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCourses/add-new', json=data_student_add_course, headers=headers)
        assert response.status_code == 201
        registeredStudentCourse=RegisteredStudentCourse.query.all()
        assert registeredStudentCourse is not None
        
    
    
    def test_api_get_registeredCourse_by_id(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCourses/add-new', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        
        response = self.client.get('/registerCourses/registeredCourse/1', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        })
        assert response.status_code == 200

        # make sure the student is in the database
        registeredCourses = RegisteredStudentCourse.query.filter_by(semester='First - Semester').first()
        assert registeredCourses is not None
        assert int(registeredCourses.id) == 1

    
    def test_api_get_all_registeredCourses(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCourses/add-new', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        
        response = self.client.get('/registerCourses/get-all', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        })
        assert response.status_code == 200

        # make sure the student is in the database
        registeredCoursesAll = RegisteredStudentCourse.query.all()
        assert registeredCoursesAll is not None
    
    
    def test_api_get_all_students_registered_in_a_particular_course(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCourses/add-new', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        #check if course_id exists
        registeredCourses=RegisteredStudentCourse.query.filter_by(course_name="Data Structures and Algorithm").first()
        
        assert registeredCourses.session_year == "2023/2024"
        course_id=registeredCourses.id
        
        response = self.client.get('/registerCourses/registeredCourse/all-students/' + str(course_id), json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        })
        assert response.status_code == 200

        # make sure the student is in the database
        registeredStudentCourseAll=RegisteredStudentCourse.query.filter(RegisteredStudentCourse.course_id==course_id).all()
        assert registeredStudentCourseAll is not None
        
    
    def test_api_update_a_registered_student_course_by_id(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCourses/add-new', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        
        response = self.client.put('/registerCourses/registeredCourse/update/1', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithms",
            "course_id": 2,
            "student":1
        })
        assert response.status_code == 200
        
    
    def test_api_delete_a_registered_student_course_by_id(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCourses/add-new', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        
        response = self.client.delete('/registerCourses/registeredCourse/delete/1', json={
            "semester":"First - Semester",
            "session_year":"2023/2024",
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "student":1
        })
        assert response.status_code == 204
