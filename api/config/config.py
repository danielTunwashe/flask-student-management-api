#setting up our configurations
import os
#After importing our secret key
from decouple import config


#Setting up our coonection string to specify the path of our database
BASE_DIR=os.path.dirname(os.path.realpath(__file__))

uri = config("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`


class Config:
    SECRET_KEY=config('SECRET_KEY','secret')
    #Specifying some configuration specific to sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')
    
    
class DevConfig(Config):
    DEBUG=config('DEBUG',cast=bool)
    #Create our connection string
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR,'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #Specifying some configuration specific to sqlite
    SQLALCHEMY_ECHO=True


class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS=False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI=uri
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DEBUG=config('DEBUG',cast=bool)

#Simple dictionary that helps us assist our classes 
config_dict={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}