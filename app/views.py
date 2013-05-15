import os, settings
from app import myApp
import uuid
from flask import request, render_template
from pdf_core import PdfHelper
from threading import Timer
from boto.s3.connection import S3Connection
from boto.s3.key import Key
           
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
        if (settings.AWS_S3_ENABLED):            
            url = upload_to_s3(uniqueFilenamePath)            
            # delete local copy
            delete(uniqueFilenamePath)
        else:        
            # remove the local file after 10 min
            t = Timer(60*10, delete, (uniqueFilenamePath,))
            t.start();  
            url = uniqueFilenamePath      
        
        # close the files
        for uploadedFile in files:
            uploadedFile.close()
                          
        return render_template('show_links.html', link=url)
    return render_template('index.html')

def upload_to_s3(filePath):
    conn = S3Connection(settings.ACCESS_KEY_ID, settings.SECRET_ACCESS_KEY)
    b = conn.get_bucket('pdfapp')
    k = Key(b)
    k.key = filePath
    #file.seek(0)
    k.set_contents_from_filename(filePath)   
    return conn.generate_url(60*10, 'GET', bucket='pdfapp', key=filePath, force_http=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in settings.ALLOWED_EXTENSIONS

def delete(dest):    
    if os.path.exists(dest):        
        os.remove(dest)