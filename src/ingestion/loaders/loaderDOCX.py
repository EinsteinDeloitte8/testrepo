from src.ingestion.loaders.loaderBase import LoaderBase
from docx import Document

class LoaderDOCX(LoaderBase):

    def __init__(self, filepath:str):
        self.filepath=filepath

    def extract_metadata(self):
        raise NotImplementedError
    
    def extract_text(self):
        raise NotImplementedError("Implement LoaderDOCX.extract_text() to extract text from a DOCX file.")