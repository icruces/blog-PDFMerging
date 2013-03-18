import os, settings
from app import app
from flask import request, render_template
from pdfCore import PdfPyPdf
from threading import Timer

# create the result folder if it doesn't exist
if not os.path.exists(os.path.dirname(settings.RESULT_PATH)): \
    os.mkdir(os.path.dirname(settings.RESULT_PATH))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in settings.ALLOWED_EXTENSIONS
           
@app.route('/', methods=['GET', 'POST'])
def upload_file():    
    if request.method == 'POST':
        # create a list with all pdf files   
        files = []      
        for uploadedFile in request.files.getlist('file'):
            if allowed_file(uploadedFile.filename):
                files.append(uploadedFile)
        
        # join pdf files
        pdfCore = PdfPyPdf()         
        pdfCore.joinPdfs(files, settings.RESULT_PATH)
        
        # remove the file after 10 min
        t = Timer(60*10, delete, (settings.RESULT_PATH,))
        t.start();        
        
        # close the files
        for uploadedFile in files:
            uploadedFile.close()
                          
        return render_template('show_links.html', link=settings.RESULT_PATH)
    return render_template('index.html')

def delete(dest):    
    if os.path.exists(dest):        
        os.remove(dest)