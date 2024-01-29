import json
import sys

from transformers import pipeline

#Preleva struttura DB da file
dbFile = open("db.json")
db = json.load(dbFile)
dbFile.close()

tables = db['database']['tabelle']

#Chiedi frase in linguaggio naturale
naturalLangPhrase = input("Inserisci frase di interrograzione in linguaggio naturale: ")

if len(naturalLangPhrase)==0:
    sys.exit("Errore: Frase in linguaggio naturale non inserita.")

#Identifica le parti del linguaggio (Parts of speech)
classifier = pipeline("token-classification", model = "sachaarbonel/bert-italian-cased-finetuned-pos")
tokens = classifier(naturalLangPhrase)

if(len(tokens)==0):
    sys.exit("Errore: impossibile interpretare la frase inserita.")

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
    if(len(foundTables) == 1):
        prompt += "Data la tabella "
    else:
        prompt += "Date le tabelle "

    for table in foundTables:
        prompt += table["nome"]+" composta dai campi "
        for field in table["campi"]:
            prompt += field["nome"]+" di tipo "+field["tipo"]+" "

    prompt += "Crea una query SQL per la seguente richiesta: "+naturalLangPhrase

else:
    print("Errore: Frase non inerente al database.")

print(prompt)