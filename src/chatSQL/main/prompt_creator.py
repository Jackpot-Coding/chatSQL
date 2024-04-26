from transformers import pipeline

from admin.models import StrutturaDatabase

from .enums import PromptGenStatus

class PromptCreator:
    
    struttura_db = 0
    
    def __init__(self,struttura_db:StrutturaDatabase):
        self.struttura_db = struttura_db                
    
    def create_prompt(self,user_request):
        # Initialize classifier
        
        classifier = pipeline("token-classification", model="sachaarbonel/bert-italian-cased-finetuned-pos")
        
        tables = self.struttura_db.tabella_set.all()

        # Tokenize natural language input
        tokens = classifier(user_request)
        
        if len(tokens)<2:
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
            prompt += f"Crea una query SQL per la seguente richiesta: {user_request}"
        
        else:
            error = "Errore: Frase non inerente al database.\n"
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
