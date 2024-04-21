from transformers import pipeline

from admin.models import StrutturaDatabase

from .enums import PromptGenStatus

class PromptCreator:
    
    struttura_db = 0
    
    def __init__(self,struttura_db:StrutturaDatabase):
        if struttura_db:
            self.struttura_db = struttura_db        
        else:
            error = f"Errore: Il database dato non esiste."
            return PromptGenStatus.DATABASE_NOT_FOUND, error
        
    
    def createPrompt(self,userRequest):
        # Initialize classifier
        
        classifier = pipeline("token-classification", model="sachaarbonel/bert-italian-cased-finetuned-pos")
        
        tables = self.struttura_db.tabella_set.all()

        # Tokenize natural language input
        tokens = classifier(userRequest)
        if not tokens:
            error = "Errore: impossibile interpretare la frase inserita."
            return PromptGenStatus.SENTENCE_UNINTERPRETABLE, error

        # Extract nouns from tokens
        nouns = [token['word'] for token in tokens if token['entity'] == 'NOUN']

        # Find relevant tables
        found_tables = self.__find_tables_from_nouns(nouns, tables)

        prompt = ""
        # Create prompt based on found tables
        if found_tables:
            
            prompt += "Data la tabella "
            
            for index, table in enumerate(found_tables):
                prompt += f"{table.nome} composta dai campi:\n"
                
                for field in table.campo_set.all():
                    field_synonyms = field.sinonimi.split(",")
                    prompt += f"-{field.nome} di tipo {field.tipo} contenente {field_synonyms[0]}\n"
                if index < len(found_tables) - 1:
                    prompt += "E la tabella "
            prompt += "\n"
            prompt += f"Crea una query SQL per la seguente richiesta: {userRequest}"
        
        else:
            error = "Errore: Frase non inerente al database.\n(Prova a cambiare la lingua in una supportata)"
            return PromptGenStatus.SENTENCE_IRRELEVANT, error

        return PromptGenStatus.SUCCESS, prompt
    
    def __find_tables_from_nouns(self,nouns,tables):
        found_tables = []
        for noun in nouns:
            for table in tables:
                synonyms = table.sinonimi.split(",")
                if noun in table.nome or noun in synonyms:
                    found_tables.append(table)
        return found_tables

# def parse_database_to_json(database_name, tables):
#     """
#     Parse database information into JSON format.
#     """
#     database_json = {
#         "database": {
#             "nome": database_name,
#             "tabelle": []
#         }
#     }
    
#     for table in tables:
#         table_info = {
#             "nome": table.nome,
#             "campi": [],
#             "sinonimi": table.sinonimi
#         }
#         fields = Campo.objects.filter(tabella=table)
#         for field in fields:
#             field_info = {
#                 "nome": field.nome,
#                 "tipo": field.tipo,
#                 "sinonimi": field.sinonimi
#             }
#             table_info["campi"].append(field_info)
#         database_json["database"]["tabelle"].append(table_info)
    
#     return database_json

# def load_database(database_name):
#     """
#     Load the database from a JSON file.
#     """
#     # Load database
#     try:
#         struttura_database = StrutturaDatabase.objects.get(nome=database_name)
#         tables = Tabella.objects.filter(struttura=struttura_database.pk)
#     except StrutturaDatabase.DoesNotExist:
#         error = f"Errore: Il database '{database_name}' non esiste."
#         return PromptGenStatus.DATABASE_NOT_FOUND, error
#     return 0, parse_database_to_json(database_name, tables) 
