import json

import logging

#Moduli Rich
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt

#Moduli LLM
from transformers import pipeline

# Set the logging level to only show errors
logging.basicConfig(level=logging.ERROR)

def load_all_databases():
    # Load the JSON data from the file
    dbFile = open("db.json", "r")
    data = json.load(dbFile)
    dbFile.close()

    # Get names of all databases
    database_names = list(data.keys())
    return database_names

classifier = pipeline("token-classification", model = "sachaarbonel/bert-italian-cased-finetuned-pos")

#console per fomattazione errore
error_console = Console(stderr=True, style="bold red")

#Preleva struttura DB da file
dbFile = open("db.json")
db = json.load(dbFile)
dbFile.close()

#Benvenuto
print(Panel(Text("Benvenuti in ChatSQL!\nInserite una frase per interrogare il database.",justify="center"), title="ChatSQL"))

# List of available databases
all_databases = load_all_databases()

# Database selection
print("Available Databases:")
for index, db_name in enumerate(all_databases, start=1):
    print(f"{index}. {db_name}")

try:
    selected_db_index = Prompt.ask("[bold blue]Select a database by entering its number")
except KeyboardInterrupt:
    error_console.print("Program interrupted. Exiting.")
    exit()

try:
    selected_db_index = int(selected_db_index)
    selected_db_name = all_databases[selected_db_index - 1]
except (ValueError, IndexError):
    error_console.print("Error: Invalid database selection.")
    exit()

# Load the selected database
with open("db.json", "r") as json_file:
    data = json.load(json_file)

selected_db = data[selected_db_name]
tables = selected_db['tabelle']

naturalLangPhrase = ""

while(len(naturalLangPhrase)==0):
    #Chiedi frase in linguaggio naturale
    try:
        naturalLangPhrase = Prompt.ask("[bold blue]Inserisci frase")
    except KeyboardInterrupt:
        error_console.print("Programma interrotto. Uscita in corso")
        exit()

    if len(naturalLangPhrase)==0:
        error_console.print("Errore: Frase in linguaggio naturale non inserita.")

#Identifica le parti del linguaggio (Parts of speech)
print("[blue]Generazione prompt...[/blue]")
tokens = classifier(naturalLangPhrase)

if(len(tokens)==0):
    error_console.print("Errore: impossibile interpretare la frase inserita.")
    exit()

#Preleva i nomi
nouns = []
for token in tokens:
    if token['entity'] == 'NOUN':
        nouns.append(token['word'])

#Trova le tabelle interessate
foundTables = []

#Cerca tabelle da nomi
for noun in nouns:
    for table in tables:
        synonyms = table['sinonimi'].split(",")
        try:
            if synonyms.index(noun)>=0:
                foundTables.append(table)
        except:
            pass

#Crea prompt dalle tabelle trovate
prompt = ""

if len(foundTables)>0:

    #Contruisci la struttura delle tabelle da interrogare
    prompt += "Data la tabella "

    for index, table in enumerate(foundTables):
        prompt += table["nome"]+" composta dai campi "
        for field in table["campi"]:
            fieldSynonyms = field["sinonimi"].split(",")
            prompt += field["nome"]+" di tipo "+field["tipo"]+" contenente "+fieldSynonyms[0]+","
        if(index < len(foundTables)-1):
            prompt += " e la tabella "

    prompt += "Crea una query SQL per la seguente richiesta: "+naturalLangPhrase

else:
    error_console.print("Errore: Frase non inerente al database.")
    exit()

#Stampa prompt e istruzioni
print(Text("Prompt Generato:\n",style="blue"))
print("[italic green]"+prompt+"\n[/italic green]")
print("Copia il testo generato in https://chat.openai.com/ per ricere la query SQL")