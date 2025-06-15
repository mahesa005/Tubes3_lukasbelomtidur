import os
import shutil
from pathlib import Path
import logging

class FileManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def ensureDirectoryExists(self, dirPath):
        try:
            Path(dirPath).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False
    
    def isValidPDF(self, filePath):
        try:
            if not os.path.exists(filePath):
                return False
            if not filePath.lower().endswith('.pdf'):
                return False
            with open(filePath, 'rb') as f:
                header = f.read(4)
                return header == b'%PDF'
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False
    
    def listPDFFiles(self, dirPath):
        pdf_files = []
        try:
            if not os.path.exists(dirPath):
                return pdf_files
            for root, dirs, files in os.walk(dirPath):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        full_path = os.path.join(root, file)
                        if self.isValidPDF(full_path):
                            pdf_files.append(full_path)
            return pdf_files
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return pdf_files
