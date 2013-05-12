import os, settings
from app import myApp
import uuid
from flask import request, render_template
from pdf_core import PdfHelper
from threading import Timer
           
@myApp.route('/', methods=['GET', 'POST'])
def upload_file():    
    if request.method == 'POST':
        # create a list with all pdf files   
        files = []      
        for uploadedFile in request.files.getlist('file'):
            if allowed_file(uploadedFile.filename):
                files.append(uploadedFile)
        
        # join pdf files
        pdfHelper = PdfHelper()  
        uniqueFilenamePath = os.path.join(settings.RESULT_PATH, str(uuid.uuid4()) + ".pdf")      
        pdfHelper.merge_pdfs(files, uniqueFilenamePath)
        
        # remove the file after 10 min
        t = Timer(60*10, delete, (uniqueFilenamePath,))
        t.start();        
        
        # close the files
        for uploadedFile in files:
            uploadedFile.close()
                          
        return render_template('show_links.html', link=uniqueFilenamePath)
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in settings.ALLOWED_EXTENSIONS

def delete(dest):    
    if os.path.exists(dest):        
        os.remove(dest)