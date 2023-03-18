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
from ..models.courses import Course
from ..models.students import Student
from ..models.registeredStudentCourses import RegisteredStudentCourse
from ..models.registeredStudentCoursesGrades import RegisteredStudentCoursesGrade
from ..models.registeredStudentCoursesGradesGpa import RegisteredStudentCoursesGradesGpa
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
        
        
    def test_api_calculate_register_courses_grade_gpa(self):
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
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":50,
            "course_name":"Linear Algebra",
            "course_id": 1,
            "course_unit":3,
            "student":1
        },headers=headers)
        assert response.status_code == 201

        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=1).all()
        assert registeredStudentCoursesGradeSingleStudent is not None
        
        for reg in registeredStudentCoursesGradeSingleStudent:
            stdID = reg.student
            response = self.client.post('/registerCoursesGradesGpa/calculate/register/gpa/' + str(stdID),headers=headers)
            assert response.status_code == 200

        
        registeredStudentCoursesGradesGpa=RegisteredStudentCoursesGradesGpa.query.all()
        assert registeredStudentCoursesGradesGpa is not None
        
    
    
    def test_api_get_all_students_registered_course_grades_gpa(self):

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
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":50,
            "course_name":"Linear Algebra",
            "course_id": 1,
            "course_unit":3,
            "student":1
        },headers=headers)
        assert response.status_code == 201

        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=1).all()
        assert registeredStudentCoursesGradeSingleStudent is not None
        
        for reg in registeredStudentCoursesGradeSingleStudent:
            stdID = reg.student
            response = self.client.post('/registerCoursesGradesGpa/calculate/register/gpa/' + str(stdID),headers=headers)
            assert response.status_code == 200
        
        response = self.client.get('/registerCoursesGradesGpa/get-all-gpa-calculated/students/all')
        assert response.status_code == 200

        registeredStudentCoursesGradesGpa=RegisteredStudentCoursesGradesGpa.query.all()
        assert registeredStudentCoursesGradesGpa is not None
        
        
    
    
    def test_api_get_all_students_registered_course_grades_gpa_by_student_id(self):

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
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":50,
            "course_name":"Linear Algebra",
            "course_id": 1,
            "course_unit":3,
            "student":1
        },headers=headers)
        assert response.status_code == 201

        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=1).all()
        assert registeredStudentCoursesGradeSingleStudent is not None
        
        for reg in registeredStudentCoursesGradeSingleStudent:
            stdID = reg.student
            response = self.client.post('/registerCoursesGradesGpa/calculate/register/gpa/' + str(stdID),headers=headers)
            assert response.status_code == 200
        
        response = self.client.get('/registerCoursesGradesGpa/get-gpa/student_id/1')
        assert response.status_code == 200

        registeredStudentCoursesGradeGpa=RegisteredStudentCoursesGradesGpa.query.filter_by(student=1).all()
        assert registeredStudentCoursesGradeGpa is not None
        
        
        
        
    def test_api_get_all_registered_student_course_grades_gpa_by_id(self):

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
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":50,
            "course_name":"Linear Algebra",
            "course_id": 1,
            "course_unit":3,
            "student":1
        },headers=headers)
        assert response.status_code == 201

        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=1).all()
        assert registeredStudentCoursesGradeSingleStudent is not None
      
        for reg in registeredStudentCoursesGradeSingleStudent:
            stdID = reg.student
            response = self.client.post('/registerCoursesGradesGpa/calculate/register/gpa/' + str(stdID),headers=headers)
            assert response.status_code == 200
            calculatedGpa = RegisteredStudentCoursesGradesGpa.query.all()
            for upstd in calculatedGpa:
                if(upstd.id==1):
                    response = self.client.get('/registerCoursesGradesGpa/get-gpa/student-by-ID/1')
                    assert response.status_code == 200
        
        
    
    def test_api_update_registered_course_grades_gpa_by_student_id(self):

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
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":50,
            "course_name":"Linear Algebra",
            "course_id": 1,
            "course_unit":3,
            "student":1
        },headers=headers)
        assert response.status_code == 201

        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=1).all()
        assert registeredStudentCoursesGradeSingleStudent is not None
      
        for reg in registeredStudentCoursesGradeSingleStudent:
            stdID = reg.student
            response = self.client.post('/registerCoursesGradesGpa/calculate/register/gpa/' + str(stdID),headers=headers)
            assert response.status_code == 200
            calculatedGpa = RegisteredStudentCoursesGradesGpa.query.filter(RegisteredStudentCoursesGradesGpa.id==1).first()
            for upstd in calculatedGpa:
                response = self.client.put('/registerCoursesGradesGpa/update/registered/gpa/' + str(upstd.id),headers=headers)
                assert response.status_code == 200
            
        


    def test_api_delete_registered_course_grades_gpa_by_student_id(self):

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
        response = self.client.post('/registerCoursesGrades/add-grades', json={
            "grade":"A",
            "score":50,
            "course_name":"Linear Algebra",
            "course_id": 1,
            "course_unit":3,
            "student":1
        },headers=headers)
        assert response.status_code == 201

        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=1).all()
        assert registeredStudentCoursesGradeSingleStudent is not None
      
        for reg in registeredStudentCoursesGradeSingleStudent:
            stdID = reg.student
            response = self.client.post('/registerCoursesGradesGpa/calculate/register/gpa/' + str(stdID),headers=headers)
            assert response.status_code == 200
            calculatedGpa = RegisteredStudentCoursesGradesGpa.query.all()
            for upstd in calculatedGpa:
                if(upstd.id==1):
                    response = self.client.delete('/registerCoursesGradesGpa/delete/1')
                    assert response.status_code == 200
        
    
    
    
    
        