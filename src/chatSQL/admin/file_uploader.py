from .parsers import csv_parser, json_parser, sql_parser

class FileUploader():
    
    def __init__(self, file):
        self.parser_strategy = None
        self.error = None
        self.set_parser_strategy(file)

    def setParserStrategy(self, file):
        if file is None:
            self.error = "Errore: nessun file caricato"
            return
        self.file = file
        if self.file.name.endswith('.csv'):
            self.parser_strategy = csv_parser.CSVParser()
        elif self.file.name.endswith('.json'):
            self.parser_strategy = json_parser.JSONParser()
        elif self.file.name.endswith('.sql'):
            self.parser_strategy = sql_parser.SQLParser()
        else:
            self.parser_strategy = None
            self.error = "Errore: formato file non supportato"
    
    def upload_file(self):
        if self.parser_strategy is None:
            return None
        return self.parser_strategy.parse(self.file)
    
    def get_status(self):
        return self.error