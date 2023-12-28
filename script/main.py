"""
<Descrizione e utilizzo script>
"""

import os
import shutil

# ///// CONFIG /////
PATH_DOCS = [
    os.path.join("docs", "src", "template.tex")
]
PATH_VERBALI_INTERNI = os.path.join("docs", "src", "verbali", "interni")
PATH_VERBALI_ESTERNI = os.path.join("docs", "src", "verbali", "esterni")

OUTPUT_NAME = "docs"
ROOT_NAME = "chatSQL"

# Inizializzati in set_directory()
ROOT_PATH = ""
TEMP_PATH = ""
OUTPUT_PATH = ""


# ///// FUNCTIONS /////

"""
Imposta correttamente le directory di root, temp e output.
Necessario perchè lo script funzioni su pc con sistemi operativi e/o 
struttura delle cartelle diversi
"""
def set_directory():
    global ROOT_PATH, TEMP_PATH, OUTPUT_PATH
    path = os.path.realpath(__file__)
    path_list = path.split(os.sep)
    path_found = False

    while not path_found:
        if path_list[-1] == ROOT_NAME:
            path_found = True
        else:
            path_list.pop()

    ROOT_PATH = os.sep.join(path_list)
    TEMP_PATH = os.path.join(ROOT_PATH, "temp")
    OUTPUT_PATH = os.path.join(ROOT_PATH, OUTPUT_NAME)
     
"""
Crea una cartella temporanea dove verranno salvati i .pdf compilati 
"""
def create_temp_directory():
    if os.path.exists(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)

    os.mkdir(TEMP_PATH)
    os.mkdir(os.path.join(TEMP_PATH, "interni"))
    os.mkdir(os.path.join(TEMP_PATH, "interni", "verbali"))
    os.mkdir(os.path.join(TEMP_PATH, "esterni"))
    os.mkdir(os.path.join(TEMP_PATH, "esterni", "verbali"))

"""
Ritorna il path alla directory corretta in base al tipo di documento
    dir_path    : directory del file .tex da compilare
"""
def get_correct_filepath(dir_path):
    path_list = dir_path.split(os.sep)

    if "verbali" in path_list:
        if "interni" in path_list:
            return os.path.join(TEMP_PATH, "interni", "verbali")
        elif "esterni" in path_list:
            return os.path.join(TEMP_PATH, "esterni", "verbali")
    else:
        if "interni" in path_list:
            return os.path.join(TEMP_PATH, "interni")
        elif "esterni" in path_list:
            return os.path.join(TEMP_PATH, "esterni")


"""
Compila il file latex e lo posiziona nella cartella temp
    dir_path    : directory del file .tex da compilare
    file_name   : nome del file .tex da compilare
"""
def compile_latex(dir_path, file_name):
    os.chdir(ROOT_PATH)
    os.chdir(dir_path)
    os.system("latexmk -pdf " + file_name)

    created_file_name = os.path.splitext(file_name)[0] + ".pdf"
    created_file_path = get_correct_filepath(dir_path)
    shutil.move(created_file_name, os.path.join(created_file_path, created_file_name))
    os.chdir(ROOT_PATH)

"""
Compila i file latex in .pdf spostandoli nella corretta cartella temp
in base al tipo di documento(interno/esterno, documento/verbale)
"""
def latex_to_pdf():
    for file_path in PATH_DOCS:
        if os.path.exists(file_path):
            dir_path, file_name = os.path.split(file_path)
            compile_latex(dir_path, file_name)


"""
Sposta i nuovi file dalla cartella temp alla cartella di output finale
"""
def move_new_files():
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.rename(TEMP_PATH, OUTPUT_PATH)

"""
Aggiorna il sito web con le nuove versioni dei file
"""
#def update_website():

"""
Messaggio finale di conferma della terminazione dello script
"""
def end_confirm():
    print("\n[ File .pdf creati in " + OUTPUT_PATH + "]\nSCRIPT TERMINATO\n")


# ///// MAIN /////

def main():
    set_directory()         # Imposta la directory dei src
    os.chdir(ROOT_PATH)     # Mi sposto nella root del progetto
    
    create_temp_directory() # Crea la cartella per i nuovi .pdf 

    latex_to_pdf()          # Crea i pdf in temp

    move_new_files()        # Sposta i nuovi file nella cartella di destinazione

    #update_website()        # Aggiorna il sito web

    end_confirm()           # Messaggio di terminazione


if __name__ == '__main__':
    main()


























