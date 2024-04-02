"""
Script per la compilazione dei file Latex in PDF
"""

import re
import os
import pathlib
import shutil
import time

# ///// CONFIG /////
PATH_DOCS = [
    os.path.join("docs", "src")
]
PATH_VERBALI_INTERNI = os.path.join("docs", "src", "verbali", "interni")
PATH_VERBALI_ESTERNI = os.path.join("docs", "src", "verbali", "esterni")

OUTPUT_NAME = "docs"
ROOT_NAME = "chatSQL"

# Inizializzati in set_directory()
ROOT_PATH   = ""
TEMP_PATH   = ""
OUTPUT_PATH = ""
SRC_PATH    = ""

# ///// FUNCTIONS /////

"""
Imposta correttamente le directory di root, temp e output.
Necessario perchè lo script funzioni su pc con sistemi operativi e/o 
struttura delle cartelle diversi
"""
def set_directory():
    global ROOT_PATH, TEMP_PATH, OUTPUT_PATH, SRC_PATH
    path = os.path.realpath(__file__)
    path_list = path.split(os.sep)
    path_found = False

    while not path_found:
        if path_list[-1] == ROOT_NAME:
            path_found = True
        else:
            path_list.pop()

    ROOT_PATH = os.sep.join(path_list)
    SRC_PATH  = os.path.join(ROOT_PATH,"docs","src");
    TEMP_PATH = os.path.join(SRC_PATH,"temp")
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
Ritorna il path alla cartella corrispondente in distribuzione
    path    : directory del file .tex da compilare
"""
def get_dist_dir_path(path):
    return path.replace(SRC_PATH,OUTPUT_PATH)

"""
Ritorna il path alla cartella temporanea corrispondente
    path    : directory del file .tex da compilare
"""
def get_temp_dir_path(path):
    return path.replace(SRC_PATH,TEMP_PATH)

def extract_version(filename):
    # Convert the filename to a string if it's a Path object
    filename_str = str(filename)
    # Use a regular expression to extract the version numbers
    match = re.search(r'-v(\d+\.\d+)', filename_str)
    if match:
        return match.group(1)
    else:
        return None

"""
Verifica se il file esistente è da ricreare
    newFile      : nuovo file da creare
    existingFile : file PDF esistente nella cartella di output
    sourceFile   : file .tex con sorgente documento
"""
def should_replace_existing_file(newFile, existingFile,sourceFile):

    if os.path.isfile(newFile):
        # Estrai nome (senza versione) dai file PDF 
        newFileName = re.sub(r'-v(\d+\.\d+)', '', os.path.splitext(newFile)[0])
        existingFileName = re.sub(r'-v(\d+\.\d+)', '', os.path.splitext(existingFile)[0])

        # Compara nomi
        if newFileName!=existingFileName: #nomi diversi = un altro documento -> non rimpiazzare
            return False
        else:
            # Estrai versione dai file PDF
            newFileVersion = extract_version(newFile)
            existingFileVersion = extract_version(existingFile)
        
            if newFileVersion != existingFileVersion: #stessi nomi e versioni diverse -> rimpiazza
                return True
            else: #file con nome e versione identiche -> controlla se .tex è più recente del PDF
                sourceFileTime       = os.path.getmtime(sourceFile)
                existingPDFFileTime  = os.path.getmtime(existingFile)
                if sourceFileTime > existingPDFFileTime:
                    return True
                else:
                    return False
    else:
        return False


"""
Elimina i file ausiliari creati da latxmk
    folder  : directory con i file ausiliari
"""
def delete_auxiliary_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


"""
Compila il file latex e lo posiziona nella cartella temp
    dir_path    : directory del file .tex da compilare
    source_file_path   : path del file .tex da compilare
"""
def compile_latex(dir_path,source_file_path):

    dist_dir = get_dist_dir_path(dir_path) # cartella di destinazione del documento
    temp_dir = get_temp_dir_path(dir_path) # cartella temporanea del documento
    
    pdf_file_name = pathlib.Path(source_file_path.replace(SRC_PATH,TEMP_PATH)).with_suffix('.pdf'); # PDF in /docs/src/temp
    pdf_dist_file_path = pathlib.Path(source_file_path.replace(SRC_PATH,OUTPUT_PATH)).with_suffix('.pdf'); #PDF in /docs/

    for existing_file in os.listdir(dist_dir): #cicla i file esistenti
        existing_file_path = os.path.join(dist_dir, existing_file)

        # Controlla se file è PDF e ha lo stesso numero di versione e elimina se si
        if os.path.isfile(existing_file_path) and existing_file.lower().endswith('.pdf') and should_replace_existing_file(pdf_dist_file_path, existing_file, source_file_path):
            os.remove(existing_file_path)

    if( not os.path.isfile(pdf_dist_file_path) ): # se il file PDF corrispondente in /docs/.. non esiste crealo

        os.chdir(ROOT_PATH)
        os.chdir(dir_path)
        os.system("latexmk -pdf -f -output-directory="+ temp_dir +" -interaction=batchmode " + source_file_path)
        print("latex for "+source_file_path)

        created_file_path = os.path.join(temp_dir,pdf_file_name)
        shutil.move(created_file_path,pdf_dist_file_path)
        delete_auxiliary_files(temp_dir)

    else:
        print("File saltato")

"""
Compila i file latex in .pdf spostandoli nella corretta cartella temp
in base al tipo di documento(interno/esterno, documento/verbale)
"""
def latex_to_pdf():
    src_walk = os.walk(SRC_PATH)
    for root,dirs,files in src_walk: # scorri la cartella /docs/src
        for folder in dirs:         # scorri cartelle in /docs/src
            if(folder != 'temp' and folder != 'assets' and folder != 'sezioni_AdR'):   
                dir_listing = os.listdir(os.path.join(root,folder))
                for file_name in dir_listing:
                    file_path = (os.path.join(root,folder,file_name))
                    if os.path.isfile(file_path):
                        if( pathlib.Path(file_path).suffix == '.tex'):
                            compile_latex(os.path.join(root,folder),file_path)



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

    # #update_website()        # Aggiorna il sito web

    end_confirm()           # Messaggio di terminazione


if __name__ == '__main__':
    main()


























