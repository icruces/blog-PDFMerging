import os, settings
from app import app
from flask import request, render_template
from pdfCore import PdfPyPdf
from threading import Timer

if not os.path.exists(settings.UPLOAD_FOLDER): os.makedirs(settings.UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in settings.ALLOWED_EXTENSIONS
           
@app.route('/', methods=['GET', 'POST'])
def upload_file():    
    if request.method == 'POST':   
        files = []      
        for uploadedFile in request.files.getlist('file'):
            if allowed_file(uploadedFile.filename):
                files.append(uploadedFile)
        
        pdfCore = PdfPyPdf()    
        dest = os.path.join(settings.UPLOAD_FOLDER, 'result.pdf')  
        pdfCore.joinPdfs(files, dest)
        t = Timer(60*10, delete, (dest,))
        t.start();
        
        
        for uploadedFile in files:
            uploadedFile.close()
                  
        return render_template('show_links.html', link=os.path.join(settings.UPLOAD_FOLDER, 'result.pdf'))
    return render_template('index.html')

def delete(dest):    
    print dest
    if os.path.exists(dest):        
        os.remove(dest)