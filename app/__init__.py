from flask import Flask
import os

app = Flask(__name__)
app.debug = True
from app import views

if settings.DEBUG == True:    
    from werkzeug.wsgi import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
          '/': os.path.join(os.path.dirname(__file__), '..')
        })