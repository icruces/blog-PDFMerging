'''
Created on 18 Nov 2012

@author: Ivan Cruces
'''
import unittest
import os
from app.pdf_core import PdfHelper
from pyPdf import PdfFileReader

class Test(unittest.TestCase):
    
    # output pdf files
    RESULT_FILE_MERGIN = "data/result.pdf"
    RESULT_FILE_SPLIT1 = "data/result1.pdf"
    RESULT_FILE_SPLIT2 = "data/result2.pdf"
    
    # input pdf files
    PDF1 = "data/a.pdf"
    PFD2 = "data/b.pdf"    
  
    def setUp(self):
        pass    
        
    def tearDown(self):
        self.__removeFile(self.RESULT_FILE_MERGIN)
        self.__removeFile(self.RESULT_FILE_SPLIT1) 
        self.__removeFile(self.RESULT_FILE_SPLIT2)    


    def testMergin(self):
              
        pdfHelper = PdfHelper()
        file1 = open(self.PDF1,"rb")
        file2 = open(self.PFD2, "rb") 
           
        assert not os.path.exists(self.RESULT_FILE_MERGIN)         
        pdfHelper.merge_pdfs((file1, file2), os.path.join('data', 'result.pdf'))
        assert os.path.exists(self.RESULT_FILE_MERGIN)
        
        pdfReader1 = PdfFileReader(file1)      
        pdfReader2 = PdfFileReader(file2)
        pdfReaderResult = PdfFileReader(file(self.RESULT_FILE_MERGIN, "rb"))

        assert pdfReader1.getNumPages() + pdfReader2.getNumPages() == pdfReaderResult.getNumPages()
        
    def testSplitPdfBasic(self):
        
        pdfHelper = PdfHelper()
        file1 = open(self.PDF1, "rb")  
        pdfReader1 = PdfFileReader(file1)
        splitPoint = pdfReader1.getNumPages()+5
                
        # the split point is upper than the number of pages        
        pdfHelper.split_pdfs(file1, splitPoint, self.RESULT_FILE_SPLIT1, self.RESULT_FILE_SPLIT2)
        assert os.path.exists(self.RESULT_FILE_SPLIT1)
        assert not os.path.exists(self.RESULT_FILE_SPLIT2)        
        pdfReaderResult = PdfFileReader(open(self.RESULT_FILE_SPLIT1))
        assert pdfReader1.getNumPages() == pdfReaderResult.getNumPages()
        
    def testSplitPdf(self):        
            
        pdfHelper = PdfHelper()
        file1 = open(self.PDF1,"rb")
        pdfReader1 = PdfFileReader(file1)        
        splitPoint = pdfReader1.getNumPages() - 2
        
        pdfHelper.split_pdfs(file1, splitPoint, self.RESULT_FILE_SPLIT1, self.RESULT_FILE_SPLIT2)
        assert os.path.exists(self.RESULT_FILE_SPLIT1)
        assert os.path.exists(self.RESULT_FILE_SPLIT2)  
        
        splitFile1 = PdfFileReader(open(self.RESULT_FILE_SPLIT1))
        splitFile2 = PdfFileReader(open(self.RESULT_FILE_SPLIT2))
        assert splitFile1.getNumPages() == splitPoint
        assert splitFile2.getNumPages() == pdfReader1.getNumPages() - splitPoint     
           
    def __removeFile(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)         

if __name__ == "__main__":    
    unittest.main()