import json
import os
from transformers import pipeline

import nltk

def generatePromptITA(natural):
    classifier = pipeline("token-classification", model = "sachaarbonel/bert-italian-cased-finetuned-pos")
    #Preleva struttura DB da file
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, 'db.json')
    dbFile = open(file_path,"r")
    db = json.load(dbFile)
    dbFile.close()
    #Preleva tabelle
    tables = db['database']['tabelle']
    tokens = classifier(natural)
    if(len(tokens)==0):
        return "Errore: impossibile interpretare la frase inserita."
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
            synonyms = table['sinonimiIt'].split(",")
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
            prompt += table["nome"]+" composta dai campi:\n"
            for field in table["campi"]:
                fieldSynonyms = field["sinonimiIt"].split(",")
                prompt +="-"+field["nome"]+" di tipo "+field["tipo"]+" contenente "+fieldSynonyms[0]+"\n"
            if(index < len(foundTables)-1):
                prompt += "E la tabella "
        prompt+="\n"
        prompt += "Crea una query SQL per la seguente richiesta: "+natural
    else:
        return "Errore: Frase non inerente al database.\n(Prova a cambiare la lingua in una supportata)"
    return prompt

def generatePromptENG(natural):
    #classifier = pipeline("token-classification", model = "vblagoje/bert-english-uncased-finetuned-pos")
    #Preleva struttura DB da file
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, 'db.json')
    dbFile = open(file_path,"r")
    db = json.load(dbFile)
    dbFile.close()
    #Preleva tabelle
    tables = db['database']['tabelle']
    tokens = nltk.word_tokenize(natural)
    parts_of_speech = nltk.pos_tag(tokens)
    nouns = list(filter(lambda x: x[1] == "NN" or x[1] == "NNS" , parts_of_speech))
    nouns = list(map(lambda x: x[0], nouns))
    if(len(nouns)==0):
        return "Error: cannot interpret input."
    #Trova le tabelle interessate
    foundTables = []
    #Cerca tabelle da nomi
    for noun in nouns:
        for table in tables:
            synonyms = table['sinonimiEn'].split(",")
            try:
                if synonyms.index(noun)>=0:
                    foundTables.append(table)
                    nouns.remove(noun)
            except:
                pass
    #Genera sinonimi per i nomi non trovati
    synonous = []
    if len(nouns)!=0:
        for noun in nouns:
            syn = nltk.corpus.wordnet.synsets(noun)
            synonous.append(noun)
            for s in syn:
                synonous.append(s.lemmas()[0].name())
                for lem in s.lemma_names():
                    synonous.append(lem)
        print(synonous)
        #Cerca tabelle da sinonimi
        for syn in synonous:
            for table in tables:
                synonyms = table['sinonimiEn'].split(",")
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
        prompt += "From table "
        for index, table in enumerate(foundTables):
            prompt += table["nome"]+" with fields:\n"
            for field in table["campi"]:
                fieldSynonyms = field["sinonimiEn"].split(",")
                prompt +="-"+field["nome"]+", type "+field["tipo"]+" with "+fieldSynonyms[0]+"\n"
            if(index < len(foundTables)-1):
                prompt += "And table "
        prompt+="\n"
        prompt += "Create a SQL query for the following request: "+natural
    else:
        return "Error: Input not database related.\n(Try changing the language to one that's supported)"
    return prompt