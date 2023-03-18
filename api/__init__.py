#Setting up our flask server
from flask import Flask
#importing our namespaces to our server
from .students.views import student_namespace
from .courses.views import course_namespace
from .registeredStudentsCourses.views import registered_students_course_namespace
from .registeredStudentsCoursesGrades.views import registered_students_course_grade_namespace
from .registeredStudentsCoursesGradeGpa.views import registered_students_course_grade_gpa_namespace
from flask_restx import Api
#importing our configuration dictionary from config folder
from .config.config import config_dict
#Import our db instance and database model to set up our tables created and also Flask_Migrate
from .utils import db
from .models.courses import Course
from .models.students import Student
from .models.registeredStudentCourses import RegisteredStudentCourse
from .models.registeredStudentCoursesGrades import RegisteredStudentCoursesGrade
from .models.registeredStudentCoursesGradesGpa import RegisteredStudentCoursesGradesGpa
from flask_migrate import Migrate
#Setting up JWT_Extended to work with our application
from flask_jwt_extended import JWTManager
#Importing packages to be used for creating custom error handler
from werkzeug.exceptions import NotFound,MethodNotAllowed






#Setting up our flask server
#Give our application factory an argument after importing our config_dict
#Create app funct helps us to create multiple instances of our application
def create_app(config=config_dict['dev']):
    #Setting up our flask server
    app=Flask(__name__)
    
    
    #Hook our configuration to our app instace, make sure it just after our main server
    app.config.from_object(config)
    
    #Protect our API With Bearer and JWT
    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':'header',
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }
    
    #impoerting our namespaces to our server (after testing we can name our API here)
    api = Api(app,
        title = "Student Management API",
        description = "A REST API for a Student Informations",
        authorizations=authorizations,
        security="Bearer Auth"
    )
    
    api.add_namespace(student_namespace)
    api.add_namespace(course_namespace)
    api.add_namespace(registered_students_course_namespace)
    api.add_namespace(registered_students_course_grade_namespace)
    api.add_namespace(registered_students_course_grade_gpa_namespace)
    
    
    #Hooking our database model to our application
    db.init_app(app)
    
    #Setting up flask migrate within our flask server
    migrate = Migrate(app,db)
    
    #Setting up our jwt_extended to our main application
    jwt=JWTManager(app)
    
    #Creating our custom error handler
    @api.errorhandler(NotFound)
    def not_found(error):
        return{"error":"Not Found"},404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return{"error":",Method Not Allowed"},405
    
    #creating a context within a shell to access our modules and db instance
    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'Student':Student,
            'Course':Course,
            'RegisteredStudentCourse':RegisteredStudentCourse,
            'RegisteredStudentCoursesGrade': RegisteredStudentCoursesGrade,
            'RegisteredStudentCoursesGradesGpa':RegisteredStudentCoursesGradesGpa
        }
    
    #setting up our flask server by returning the app
    return app