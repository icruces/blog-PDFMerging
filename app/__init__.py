from flask import Flask
import os, settings

myApp = Flask(__name__)
myApp.debug = settings.DEBUG
from app import views

# create the result folder if it doesn't exist
if not os.path.exists(settings.RESULT_PATH): \
    os.mkdir(settings.RESULT_PATH)
    
if settings.DEBUG == True:
    from werkzeug.wsgi import SharedDataMiddleware
    myApp.wsgi_app = SharedDataMiddleware(myApp.wsgi_app, {
          '/data': os.path.join(os.path.dirname(__file__), '../data')
        })
