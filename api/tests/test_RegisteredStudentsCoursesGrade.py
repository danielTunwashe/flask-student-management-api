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
from ..models.registeredStudentCoursesGrades import RegisteredStudentCoursesGrade
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
        
        
    
    def test_api_add_registered_courses_grade(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "course_unit":1,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        
        
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None
        
        
    
    
    def test_api_get_all_registered_courses_grades(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "course_unit": 2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None
        
        response = self.client.get('/registerCoursesGrades/get-all-grades', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "course_unit":2,
            "student":1
        })
        assert response.status_code == 200
        registeredCoursesGrades = RegisteredStudentCoursesGrade.query.filter_by(course_name='Data Structures and Algorithm').first()
        assert registeredCoursesGrades is not None
        
        
    def test_api_update_a_registered_courses_grade_by_id(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "course_unit":2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None
        
        response = self.client.put('/registerCoursesGrades/update/1', json={
            "grade":"A",
            "score":80,
            "course_name":"Data Structures and Algorithms",
            "course_id": 2,
            "course_unit":2,
            "student":1
        })
        assert response.status_code == 200
        
        
        
    def test_api_delete_a_registered_courses_grade_by_id(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "course_unit":2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None
        
        response = self.client.delete('/registerCoursesGrades/delete/1', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "course_unit":2,
            "student":1
        })
        assert response.status_code == 204
        
        
    
    def test_api_get_all_registered_courses_grades_in_a_particular_course(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 2,
            "course_unit":2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"B",
            "score":50,
            "course_name":"Theory of Automata",
            "course_id": 2,
            "course_unit":2,
            "student":2
        },headers=headers)
        assert response.status_code == 201
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None
        course_id=2
        
        response = self.client.get('/registerCoursesGrades/get-all-students-grades/' + str(course_id))
        assert response.status_code == 200
        registeredStudentCoursesGradeAll=RegisteredStudentCoursesGrade.query.filter(RegisteredStudentCoursesGrade.course_id==course_id).all()
        assert registeredStudentCoursesGradeAll is not None
        
    
    
    def test_api_get_a_particular_registered_student_grades_in_all_courses(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":70,
            "course_name":"Data Structures and Algorithm",
            "course_id": 1,
            "course_unit":2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"B",
            "score":50,
            "course_name":"Theory of Automata",
            "course_id": 2,
            "course_unit":2,
            "student":1
        },headers=headers)
        assert response.status_code == 201
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        assert registeredStudentCoursesGrade is not None

        
        response = self.client.get('/registerCoursesGrades/get-grade/student/1/all-courses')
        assert response.status_code == 200
        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=2).all()
        assert registeredStudentCoursesGradeSingleStudent is not None
    
    
    
    
        
    
    
    
    
    
    
        
        
        

        
    