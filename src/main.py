import json

#Moduli Rich
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt

#Moduli NLP
from pattern3.text.it import singularize
from pattern3.text.it import pluralize
from PyMultiDictionary import MultiDictionary
dictionary = MultiDictionary()

#Moduli LLM
from transformers import pipeline

classifier = pipeline("token-classification", model = "sachaarbonel/bert-italian-cased-finetuned-pos")

#console per fomattazione errore
error_console = Console(stderr=True, style="bold red")

#Preleva struttura DB da file
dbFile = open("db.json")
db = json.load(dbFile)
dbFile.close()
#Preleva tabelle
tables = db['database']['tabelle']

#Benvenuto
print(Panel(Text("Benvenuti in ChatSQL!\nInserite una frase per interrogare il database.",justify="center"), title="ChatSQL"))
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
                nouns.remove(noun)
        except:
            pass

#print(nouns)

#Genera sinonimi per i nomi non trovati
synonous = []
if len(nouns)!=0:
    for noun in nouns:
        singularized_noun = singularize(noun)
        syn = dictionary.synonym('it', singularized_noun)
        synonous.append(pluralize(singularized_noun))
        for s in syn:
            synonous.append(s)
            synonous.append(pluralize(s))
    
    #print(synonous)
    #Cerca tabelle da sinonimi
    for syn in synonous:
        for table in tables:
            synonyms = table['sinonimi'].split(",")
            try:
                if synonyms.index(syn)>=0:
                    foundTables.append(table)
                    synonous.remove(syn)
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
            prompt += field["nome"]+" di tipo "+field["tipo"]+" "
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
