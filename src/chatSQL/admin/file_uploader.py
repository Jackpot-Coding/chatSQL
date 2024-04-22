from .parsers import csv_parser, json_parser

class FileUploader():
    
    def __init__(self, file):
        self.parserStrategy = None
        self.setParserStrategy(file)

    def setParserStrategy(self, file):
        self.file = file
        if self.file.name.endswith('.csv'):
            self.parserStrategy = csv_parser.CSVParser()
        elif self.file.name.endswith('.json'):
            self.parserStrategy = json_parser.JSONParser()     
    
    def uploadFile(self):
        return self.parserStrategy.parser(self.file)