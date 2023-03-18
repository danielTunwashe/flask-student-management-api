#Creating our namespaces from flask_restx to access our Resources class which will be used as blueprints
from flask_restx import Resource,Namespace,fields
#importing request from flask to access our data from the client
from flask import request
#importing our student class to create a new instance of our student
from ..models.students import Student
from ..models.courses import Course
from ..models.registeredStudentCoursesGrades import RegisteredStudentCoursesGrade
#Importing HTTP satus code from HTTP
from http import HTTPStatus
#Importing access token and refresh token to create a JWT Identity
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
#importing sql-alchemy instance from utils
from ..utils import db




#Creating our namespace to seperate our application
registered_students_course_grade_namespace = Namespace('registerCoursesGrades',description="A namespace for registering student registered courses grades")


#Createing a module for serialization (import fields from flask_restx)
registeredStudentCoursesGrade_model=registered_students_course_grade_namespace.model(
    'RegisteredStudentCoursesGrade',{
        'id':fields.Integer(description="An ID"),
        'grade':fields.String(description="Expecting a grade (eg: A or B or C)"),
        'score':fields.Integer(description="Expecting a score (eg: 90, 70, 30 )",required=True),
        'course_name':fields.String(description="Name of the course you want to grade",required=True),
        'course_id':fields.Integer(description="Course ID",required=True),
        'course_unit':fields.Integer(description="Course Unit",required=True),
        'student':fields.Integer(description="Student ID")
    }
)


#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_namespace.route('/add-grades')
class registerCoursesGrades(Resource):
    #Protect our endpoint and since we want a new refresh token we have to set it to be True
    @jwt_required()
    #Decorator to help us expect the information in our serilizer in order to send data to our API
    @registered_students_course_grade_namespace.expect(registeredStudentCoursesGrade_model)
    #Return our response via flask restx and the module created
    @registered_students_course_grade_namespace.marshal_with(registeredStudentCoursesGrade_model)
    @registered_students_course_grade_namespace.doc(
        description="Student Add Registered Courses Grades"
    )
    def post(self):

        '''
            Register registered courses grades / add registered courses grades
        '''
        email=get_jwt_identity()
        #Querying the student table to get the stuend email
        current_student=Student.query.filter_by(email=email).first()

        

        #Gets the data that comes from registeredStudentCourse as json so we return the ID of the course
        datastd = request.get_json()
        
        #Get the course name registered through our datastd and set course_id=0
        course_name=datastd.get('course_name') 
        course_id=0
        course_unit=0
        
        #Getting the score of the inputed course
        score = int(datastd.get('score'))
        
        gradeCalc = ""
        
        scoredict={
            "A":100,
            "B":69,
            "C":59,
            "D":49,
            "E":44,
            "F":39
        }
        
        #Calculate the grade based on scores provided
        # print(scoredict)
        # print(scoredict["A"] + scoredict["B"])
        key_list=list(scoredict.keys())
        # print(key_list[3])
        if((score > scoredict["B"]) and (score <= scoredict["A"])):
            gradeCalc = key_list[0]
        elif((score > scoredict["C"]) and (score <= scoredict["B"])):
            gradeCalc = key_list[1]
        elif((score > scoredict["D"]) and (score <= scoredict["C"])):
            gradeCalc = key_list[2]
        elif((score > scoredict["E"]) and (score <= scoredict["D"])):
            gradeCalc = key_list[3]
        elif((score > scoredict["F"]) and (score <= scoredict["E"])):
            gradeCalc = key_list[4]
        else:
            gradeCalc = key_list[5]
        
        
        #Scan the database and check if the gotten course name exist and return the ID 
        results = db.session.query(Course).filter(Course.course_name==course_name)
        for course in results:
            course_id=course.id
            course_unit=course.course_unit
        
        
        
        #Access the data from our student through our registered_students_course_namespace.payload (similar to request.getjson from flask)
        data = registered_students_course_grade_namespace.payload
        

        #Using the payload data which is a dictionary to create our post
        new_registeredStudentCourseGrade=RegisteredStudentCoursesGrade(
            grade=gradeCalc,
            score=data['score'],
            course_name=data['course_name'],
            course_unit=course_unit,
            course_id=course_id
        )
        #specify the student who registered for the course (via the relationship between the student and the registeredStudentCourse table using the backref in our Student table) import get_jwt_identity
        new_registeredStudentCourseGrade.studentGrade=current_student
 
        
        #save our post to the database
        new_registeredStudentCourseGrade.save()
        
        return new_registeredStudentCourseGrade, HTTPStatus.CREATED
        


#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_namespace.route('/get-all-grades')
class GetAllregisteredStudentsCoursesGrades(Resource):
    #Want the object returned to be returned as json
    @registered_students_course_grade_namespace.marshal_with(registeredStudentCoursesGrade_model)
    @registered_students_course_grade_namespace.doc(
        description="Get/Retrieve all Student Registered Courses Grades"
    )
    def get(self):
        '''
            Get all registered students courses grades
        '''
        #First create a module that helps us serilaize the data we pass to our API as well as help us marshal our responses and then, our responses will be return as json 
        #Query all registered student course from our database (import our registeredStudentCourse from models)
        registeredStudentCoursesGrade=RegisteredStudentCoursesGrade.query.all()
        # for registeredCourses in registeredStudentCourse:
        #     print(registeredCourses.studentCourse.id)
        #Return all courses (return user returns all course as objects which is not json serializable) - (Import our HTTP status class from http)
        return registeredStudentCoursesGrade, HTTPStatus.OK
        


#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_namespace.route('/update/<int:registeredStudentsCoursesGrades_id>')
class updateregisterdStudentsCoursesGrades(Resource):
    #Decorator to help us expect the information in our serilizer in order to send data to our API
    @registered_students_course_grade_namespace.expect(registeredStudentCoursesGrade_model)
    #Return our response via flask restx and the module created
    @registered_students_course_grade_namespace.marshal_with(registeredStudentCoursesGrade_model)
    @registered_students_course_grade_namespace.doc(
        description="Update a Registered Student Courses Grades by ID",
        params={
            "registeredStudentsCoursesGrades_id":"An ID for updating a registered student course grade"
        }
    )
    def put(self,registeredStudentsCoursesGrades_id):
        '''
            Update a registered student courses grades by ID
        '''
        #First get registeredStudentCoursesGrade ID
        studentRegisteredCoursesGrade_to_update=RegisteredStudentCoursesGrade.get_by_id(registeredStudentsCoursesGrades_id)
        
        #Gets the data that comes from studentRegisteredCoursesGrade_to_update as json
        data = request.get_json()
        #Gets the data that comes from registeredStudentCourse as json so we return the ID of the course
        datastd = request.get_json()
        
        #Get the course name registered through our datastd and set course_id=0
        course_name=data.get('course_name') 
        course_id=0
        course_unit=0
        
        
        
        #Getting the score of the inputed course
        score = int(datastd.get('score'))
        
        gradeCalc = ""
        
        scoredict={
            "A":100,
            "B":69,
            "C":59,
            "D":49,
            "E":44,
            "F":39
        }
        
        #Calculate the grade based on scores provided
        # print(scoredict)
        # print(scoredict["A"] + scoredict["B"])
        key_list=list(scoredict.keys())
        # print(key_list[3])
        if((score > scoredict["B"]) and (score <= scoredict["A"])):
            gradeCalc = key_list[0]
        elif((score > scoredict["C"]) and (score <= scoredict["B"])):
            gradeCalc = key_list[1]
        elif((score > scoredict["D"]) and (score <= scoredict["C"])):
            gradeCalc = key_list[2]
        elif((score > scoredict["E"]) and (score <= scoredict["D"])):
            gradeCalc = key_list[3]
        elif((score > scoredict["F"]) and (score <= scoredict["E"])):
            gradeCalc = key_list[4]
        else:
            gradeCalc = key_list[5]
        
        
        
        #Scan the database and check if the gotten course name exist and return the ID 
        results = db.session.query(Course).filter(Course.course_name==course_name)
        for course in results:
            course_id=course.id
            course_unit=course.course_unit
        
        #Update our user due to different data that comes from our json endpoint
        studentRegisteredCoursesGrade_to_update.grade=gradeCalc
        studentRegisteredCoursesGrade_to_update.score=data.get('score')
        studentRegisteredCoursesGrade_to_update.course_name=data.get('course_name')
        studentRegisteredCoursesGrade_to_update.course_id=course_id
        studentRegisteredCoursesGrade_to_update.course_unit=course_unit

        #Save to our database (import our sqlAlchemy instance from utils)
        db.session.add(studentRegisteredCoursesGrade_to_update)
        db.session.commit()
        
        #return the updated student (we have to marshal with student_model) 
        return studentRegisteredCoursesGrade_to_update, HTTPStatus.OK

#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_namespace.route('/delete/<int:registeredStudentsCoursesGrades_id>')
class deleteregisterdStudentsCoursesGrades(Resource):
    #Make the object returned json serilizable
    @registered_students_course_grade_namespace.marshal_with(registeredStudentCoursesGrade_model)
    @registered_students_course_grade_namespace.doc(
        description="Delete A Registered Coureses Grades by ID",
        params={
            "registeredStudentsCoursesGrades_id":"An ID for deleting a registered student course grade"
        }
    )
    def delete(self,registeredStudentsCoursesGrades_id):
        '''
            Delete a registered student courses grades by ID
        '''
        
        #Query for the registeredStudentCoursesGrade to delete 
        registeredStudentCoursesGrade_to_delete = RegisteredStudentCoursesGrade.get_by_id(registeredStudentsCoursesGrades_id)
        
        #Use the simple method in the RegisteredStudentCoursesGrade model to delete easily
        registeredStudentCoursesGrade_to_delete.delete()
        
        #return a response
        return registeredStudentCoursesGrade_to_delete, HTTPStatus.NO_CONTENT
    
    
      
      
#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_namespace.route('/get-all-students-grades/<int:course_id>')
class getAllRegisteredStudentsGradesInAParticularCourse(Resource):
    @registered_students_course_grade_namespace.marshal_with(registeredStudentCoursesGrade_model)
    @registered_students_course_grade_namespace.doc(
        description="Get all Registered Student Grades in a Particular Course",
        params={
            "course_id":"An ID for Getting all registered Student grades in a particular course"
        }
    )
    def get(self,course_id):
        '''
            Get/Retrieve all registered students grades in a particular course
        '''
        
        #Filter the registeredStudentCoursesGrade database by the course_id and returns all  
        registeredStudentCoursesGradeAll=RegisteredStudentCoursesGrade.query.filter(RegisteredStudentCoursesGrade.course_id==course_id).all()
        
        #Return our registeredStudentCourse and HTTP status
        return registeredStudentCoursesGradeAll,HTTPStatus.OK
        

            

# #import resource class and create our class that inherits from our resource class
# @registered_students_course_grade_namespace.route('/get-grade/student/<int:student_id>/course/<int:course_id>')
# class getAParticularRegisteredStudentsGradesInAParticularCourse(Resource):
#     @registered_students_course_grade_namespace.marshal_with(registeredStudentCoursesGrade_model)
#     def get(self,student_id,course_id):
#         '''
#             Get a particular registered student grade in a particular course
#         '''
#         registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=student_id).all()
#         for reg in registeredStudentCoursesGradeSingleStudent:
#              if(reg.student==course_id):
#                  print(reg)
        
#         return registeredStudentCoursesGradeSingleStudent,HTTPStatus.OK
    
    
    

#import resource class and create our class that inherits from our resource class
@registered_students_course_grade_namespace.route('/get-grade/student/<int:student_id>/all-courses')
class getAParticularRegisteredStudentsGradesInAllCourses(Resource):
    @registered_students_course_grade_namespace.marshal_with(registeredStudentCoursesGrade_model)
    @registered_students_course_grade_namespace.doc(
        description="Get/Retrieve a particular Registered Student Courses Grades in all Courses",
        params={
            "student_id":"An ID for Getting a particular registered Student grades in a all courses"
        }
    )
    def get(self,student_id):
        '''
            Get a particular registered student grades in each courses registered
        '''     
        #Read the rows in RegisteredStudentCoursesGrade
        # reg = RegisteredStudentCoursesGrade.query.filter_by(student=student_id).all()
  
        registeredStudentCoursesGradeSingleStudent=RegisteredStudentCoursesGrade.query.filter_by(student=student_id).all()
        # for reg in registeredStudentCoursesGradeSingleStudent:
        #     print(reg.student)
        
        #Return our registeredStudentCourse and HTTP status
        return registeredStudentCoursesGradeSingleStudent,HTTPStatus.OK
        
        
        
        

# #import resource class and create our class that inherits from our resource class
# @registered_students_course_grade_namespace.route('/update/student/<int:student_id>')
# class UpdateStudentRegisteredCoursesGrades(Resource):
#     def put(self,student_id):
#         '''
#             Update a particular student registered courses grades by student ID
#         '''
        

