
#!flask/bin/python
from app import myApp
import os
port = int(os.environ.get('PORT', 5000))

myApp.run(host='0.0.0.0', port=port)


