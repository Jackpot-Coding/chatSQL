from .parsers import csv_parser, json_parser

class FileUploader():
    
    def __init__(self, file):
        self.parserStrategy = None
        self.error = None
        self.setParserStrategy(file)

    def setParserStrategy(self, file):
        if file is None:
            self.error = "Errore: nessun file caricato"
            return
        self.file = file
        if self.file.name.endswith('.csv'):
            self.parserStrategy = csv_parser.CSVParser()
        elif self.file.name.endswith('.json'):
            self.parserStrategy = json_parser.JSONParser()
        else:
            self.parserStrategy = None
            self.error = "Errore: formato file non supportato"
    
    def uploadFile(self):
        if self.parserStrategy is None:
            return None
        return self.parserStrategy.parser(self.file)
    
    def getStatus(self):
        return self.error