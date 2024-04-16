from transformers import pipeline

from admin.models import Campo, StrutturaDatabase, Tabella

from .enums import PromptGenStatus

def parse_database_to_json(database_name, tables):
    """
    Parse database information into JSON format.
    """
    database_json = {
        "database": {
            "nome": database_name,
            "tabelle": []
        }
    }
    
    for table in tables:
        table_info = {
            "nome": table.nome,
            "campi": []
        }
        fields = Campo.objects.filter(tabella=table)
        for field in fields:
            field_info = {
                "nome": field.nome,
                "tipo": field.tipo,
                "sinonimiIt": field.sinonimi
            }
            table_info["campi"].append(field_info)
        database_json["database"]["tabelle"].append(table_info)
    
    return database_json

def load_database(database_name):
    """
    Load the database from a JSON file.
    """
    # Load database
    try:
        struttura_database = StrutturaDatabase.objects.get(nome=database_name)
        tables = Tabella.objects.filter(struttura=struttura_database)
    except StrutturaDatabase.DoesNotExist:
        error = f"Errore: Il database '{database_name}' non esiste."
        return PromptGenStatus.DATABASE_NOT_FOUND, error
    return 0, parse_database_to_json(database_name, tables) 

def find_tables_from_nouns(nouns, tables):
    """
    Find tables based on noun synonyms.
    """
    found_tables = []
    for noun in nouns:
        for table in tables:
            synonyms = table['sinonimiIt'].split(",")
            if noun in synonyms:
                found_tables.append(table)
    return found_tables

def generate_prompt_ita(natural, database_name):
    """
    Generate a prompt in Italian based on the given natural language input.
    """

    # Initialize classifier
    classifier = pipeline("token-classification", model="sachaarbonel/bert-italian-cased-finetuned-pos")

    # Load database
    db = load_database(database_name)
    if db[0] == PromptGenStatus.DATABASE_NOT_FOUND:
        return db
    
    tables = db[1]['database']['tabelle']

    # Tokenize natural language input
    tokens = classifier(natural)
    if not tokens:
        error = "Errore: impossibile interpretare la frase inserita."
        return PromptGenStatus.SENTENCE_UNINTERPRETABLE, error

    # Extract nouns from tokens
    nouns = [token['word'] for token in tokens if token['entity'] == 'NOUN']

    # Find relevant tables
    found_tables = find_tables_from_nouns(nouns, tables)

    prompt = ""
    # Create prompt based on found tables
    if found_tables:
        prompt += "Data la tabella "
        for index, table in enumerate(found_tables):
            prompt += f"{table['nome']} composta dai campi:\n"
            for field in table["campi"]:
                field_synonyms = field["sinonimiIt"].split(",")
                prompt += f"-{field['nome']} di tipo {field['tipo']} contenente {field_synonyms[0]}\n"
            if index < len(found_tables) - 1:
                prompt += "E la tabella "
        prompt += "\n"
        prompt += f"Crea una query SQL per la seguente richiesta: {natural}"
    else:
        error = "Errore: Frase non inerente al database.\n(Prova a cambiare la lingua in una supportata)"
        return PromptGenStatus.SENTENCE_IRRELEVANT, error

    return PromptGenStatus.SUCCESS, prompt
