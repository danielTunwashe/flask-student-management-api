#Creating our namespaces from flask_restx to access our Resources class which will be used as blueprints
from flask_restx import Resource,Namespace,fields
#importing request from flask to access our data from the client
from flask import request
#importing our student class to create a new instance of our student
from ..models.students import Student
from ..models.courses import Course
from ..models.registeredStudentCoursesGrades import RegisteredStudentCoursesGrade
from ..models.registeredStudentCoursesGradesGpa import RegisteredStudentCoursesGradesGpa
#Importing HTTP satus code from HTTP
from http import HTTPStatus
#Importing access token and refresh token to create a JWT Identity
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
#importing sql-alchemy instance from utils
from ..utils import db


#Creating our namespace to seperate our application
registered_students_course_grade_gpa_namespace = Namespace('registerCoursesGradesGpa',description="A namespace for registering student registered courses grades GPA")


#Createing a module for serialization (import fields from flask_restx)
registeredStudentCoursesGradesGpa_model=registered_students_course_grade_gpa_namespace.model(
    'RegisteredStudentCoursesGradesGpa',{
        'id':fields.Integer(description="An ID"),
        'gpa':fields.Float(description="Expecting a gpa (eg: 4.5, 5.0, 3.26 etc)"),
        'semester':fields.String(description="Expecting a semester eg(First - Semester)"),
        'session_year':fields.String(description="Expecting a session_year(eg: 2023/2024)")
    }
)



#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_gpa_namespace.route('/calculate/register/gpa/<int:student_id>')
class CalculateRegisterGpa(Resource):
    #Protect our endpoint and since we want a new refresh token we have to set it to be True
    @jwt_required()
    @registered_students_course_grade_gpa_namespace.marshal_with(registeredStudentCoursesGradesGpa_model)
    @registered_students_course_grade_gpa_namespace.doc(
        description="Calculate and Store a Student Gpa by ID",
        params={
            "student_id":"An ID to calculate registered courses grades GPA"
        }
    )
    def post(self,student_id):
        '''
            calulate and register registered courses grades gpa
        '''
        
        email=get_jwt_identity()
        #Querying the student table to get the stuend email
        current_student=Student.query.filter_by(email=email).first()

        
        #Get a particular student registered courses grades by ID
        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=student_id).all()
                
                
        #GPA LOGIC BEGINS...
        gpaCalc=0
        tcp=0
        tcu=0
        gradeMarkDict={
            "A":5,
            "B":4,
            "C":3,
            "D":2,
            "E":1,
            "F":0
        }
        
        
        for reg in registeredStudentCoursesGradeSingleStudent:
            if(reg.grade=="A"):
                tcp+=(gradeMarkDict["A"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="B"):
                tcp+=(gradeMarkDict["B"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="C"):
                tcp+=(gradeMarkDict["C"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="D"):
                tcp+=(gradeMarkDict["D"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="E"):
                tcp+=(gradeMarkDict["E"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            else:
                tcp+=(gradeMarkDict["F"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
        print(tcu)
        gpaCalc=float('%.3g' % (tcp/tcu))
        #GPA LOGIC ENDS...
        
        
        #Access the data from our student through our registered_students_course_namespace.payload (similar to request.getjson from flask)
        data = registered_students_course_grade_gpa_namespace.payload
        
        #Using the payload data which is a dictionary to create our new_registeredStudentCourseGradesGpa
        new_registeredStudentCourseGradesGpa=RegisteredStudentCoursesGradesGpa(
            gpa=float(gpaCalc),
            semester=data['semester'],
            session_year=data['session_year']
        )
        
        #specify the student who registered for the GPA (via the relationship between the student and the registeredStudentCoursesGradeGpa table using the backref in our Student table) import get_jwt_identity
        new_registeredStudentCourseGradesGpa.studentGradeGpa=current_student
        
        #save our gpa to the database
        new_registeredStudentCourseGradesGpa.save()
        
        #Return our registeredStudentCourse and HTTP status
        return new_registeredStudentCourseGradesGpa,HTTPStatus.OK
        
       
        
        
#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_gpa_namespace.route('/get-all-gpa-calculated/students/all')
class getAllRegisteredStudentsCoursesGradesGpa(Resource):
    #Want the object returned to be returned as json
    @registered_students_course_grade_gpa_namespace.marshal_with(registeredStudentCoursesGradesGpa_model)
    @registered_students_course_grade_gpa_namespace.doc(
        description="Get all Student Registered Courses Gpa scores"
    )
    def get(self):
        '''
            Get all students registered courses grades GPA
        '''
        
        #Query registeredStudentCoursesGradesGpa tbl
        registeredStudentCoursesGradesGpa=RegisteredStudentCoursesGradesGpa.query.all()

        #Returns results of query
        return registeredStudentCoursesGradesGpa, HTTPStatus.OK


#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_gpa_namespace.route('/get-gpa/student_id/<int:student_id>')
class getAllRegisteredStudentsCoursesGradesGpa(Resource):
    #Make the object returned json serializable
    @registered_students_course_grade_gpa_namespace.marshal_with(registeredStudentCoursesGradesGpa_model)
    @registered_students_course_grade_gpa_namespace.doc(
        description="Get a Particular Registered Courses Gpa by Student - ID",
        params={
            "student_id":"An ID for getting a particular student Gpa"
        }
    )
    def get(self,student_id):
        '''
            Get a particular students registered courses grades GPA by Student ID
        '''
        #Get a particular student registered courses grades by ID
        registeredStudentCoursesGradeGpa=RegisteredStudentCoursesGradesGpa.query.filter_by(student=student_id).all()
        
        #Return our registeredStudentCourse and HTTP status
        return registeredStudentCoursesGradeGpa,HTTPStatus.OK
    

    
    
#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_gpa_namespace.route('/update/registered/gpa/<int:student_id>')
class UpdateCalculatedRegisteredGpa(Resource):
    #Make the object returned json serializable
    @registered_students_course_grade_gpa_namespace.marshal_with(registeredStudentCoursesGradesGpa_model)
    #Protect our endpoint and since we want a new refresh token we have to set it to be True
    @jwt_required()
    @registered_students_course_grade_gpa_namespace.doc(
        description="Update Stored Registered Courses Gpa by Student - ID",
        params={
            "student_id":"An ID for updating calculated registered student student Gpa"
        }
    )
    def put(self,student_id):
        '''
            update calculated registered courses grades gpa by student ID
        '''
        
        email=get_jwt_identity()
        #Querying the student table to get the stuend email
        current_student=Student.query.filter_by(email=email).first()

        
        #Get a particular student registered courses grades by ID
        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=student_id).all()
                
        
        #First get registeredStudentCoursesGradesGpa ID
        studentRegisteredCoursesGradesGpa_to_update=RegisteredStudentCoursesGradesGpa.get_by_id(student_id)
                
        #Gets the data that comes from studentRegisteredCoursesGrade_to_update as json
        data = request.get_json()
        
        #GPA LOGIC BEGINS...
        gpaCalc=0
        tcp=0
        tcu=0
        gradeMarkDict={
            "A":5,
            "B":4,
            "C":3,
            "D":2,
            "E":1,
            "F":0
        }
        
        
        for reg in registeredStudentCoursesGradeSingleStudent:
            if(reg.grade=="A"):
                tcp+=(gradeMarkDict["A"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="B"):
                tcp+=(gradeMarkDict["B"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="C"):
                tcp+=(gradeMarkDict["C"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="D"):
                tcp+=(gradeMarkDict["D"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            elif(reg.grade=="E"):
                tcp+=(gradeMarkDict["E"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
            else:
                tcp+=(gradeMarkDict["F"]*int(reg.course_unit))
                tcu+=int(reg.course_unit)
        
        gpaCalc=float('%.3g' % (tcp/tcu))
        #GPA LOGIC ENDS...
        
        studentRegisteredCoursesGradesGpa_to_update.gpa=float(gpaCalc)
        studentRegisteredCoursesGradesGpa_to_update.semester=data.get('semester')
        studentRegisteredCoursesGradesGpa_to_update.session_year=data.get('session_year')

        
        #specify the student who registered for the GPA (via the relationship between the student and the registeredStudentCoursesGradeGpa table using the backref in our Student table) import get_jwt_identity
        studentRegisteredCoursesGradesGpa_to_update.studentGradeGpa=current_student
        
        #Save to our database (import our sqlAlchemy instance from utils)
        db.session.add(studentRegisteredCoursesGradesGpa_to_update)
        db.session.commit()
        
        #Return our registeredStudentCourse and HTTP status
        return studentRegisteredCoursesGradesGpa_to_update,HTTPStatus.OK
    
#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_gpa_namespace.route('/delete/<int:registeredStudentsCoursesGradesGpa_id>')
class deleteregisterdStudentsCoursesGrades(Resource):
    #Make the object returned json serilizable
    @registered_students_course_grade_gpa_namespace.marshal_with(registeredStudentCoursesGradesGpa_model)
    @registered_students_course_grade_gpa_namespace.doc(
        description="Delete a Registered Student Courses Gpa by ID",
        params={
            "registeredStudentsCoursesGradesGpa_id":"An ID for deleting a registered student Gpa"
        }
    )
    def delete(self,registeredStudentsCoursesGradesGpa_id):
        '''
            Delete a registered student courses grades Gpa by ID
        '''
        
        #Query for the registeredStudentCoursesGrade to delete 
        registeredStudentCoursesGradesGpa_to_delete = RegisteredStudentCoursesGradesGpa.get_by_id(registeredStudentsCoursesGradesGpa_id)
        
        #Use the simple method in the RegisteredStudentCoursesGrade model to delete easily
        registeredStudentCoursesGradesGpa_to_delete.delete()
        
        #return a response
        return registeredStudentCoursesGradesGpa_to_delete, HTTPStatus.NO_CONTENT