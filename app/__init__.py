from flask import Flask
import os, settings

app = Flask(__name__)
app.debug = settings.DEBUG
from app import views

# create the result folder if it doesn't exist
if not os.path.exists(settings.RESULT_PATH): \
    os.mkdir(settings.RESULT_PATH)
    
if settings.DEBUG == True:
    from werkzeug.wsgi import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
          '/': os.path.join(os.path.dirname(__file__), '.')
        })
