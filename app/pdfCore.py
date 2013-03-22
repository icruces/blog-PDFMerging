from pyPdf import PdfFileReader, PdfFileWriter

class PdfPyPdf:
    '''    
    Class for merging and splitting pdf files.    
    '''
    
    def __init__(self):
        pass
    
    def joinPdfs(self, files, dest="result.pdf"):
                      
        # merge the collection of files
        output = PdfFileWriter()
        for pdfFile in files:
            pdfReader = PdfFileReader(pdfFile) 
            for i in range(0, pdfReader.getNumPages()):
                output.addPage(pdfReader.getPage(i))       
        
        outputStream = open(dest, "wb")
        output.write(outputStream)
        outputStream.close()
        
    def splitPdf(self, pdfFile, splitPoint, dest1="result_1.pdf", dest2="result_2.pdf"):
        
        pdfReader = PdfFileReader(pdfFile)
        if (pdfReader.getNumPages() <= splitPoint):       
            self.__createPdf(pdfReader, 0, pdfReader.getNumPages(), dest1)
        else:        
            self.__createPdf(pdfReader, 0, splitPoint, dest1)
            self.__createPdf(pdfReader, splitPoint, pdfReader.getNumPages(), dest2) 
            
    def __createPdf(self, pdfReader, firstIndex, lastIndex, outputName):
        
        output = PdfFileWriter()
        for i in range(firstIndex, lastIndex):
            output.addPage(pdfReader.getPage(i))
            
        outputStream = file(outputName, "wb")
        output.write(outputStream)
        outputStream.close()