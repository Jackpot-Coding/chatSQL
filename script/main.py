"""
<Descrizione e utilizzo script>
"""

import os
import pathlib
import shutil

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
    file_name   : nome del file .tex da compilare
"""
def compile_latex(dir_path,file_name):

    dist_dir = get_dist_dir_path(dir_path) # cartella di destinazione del documento
    temp_dir = get_temp_dir_path(dir_path) # cartella temporanea del documento
    
    p = pathlib.Path(file_name)
    pdf_file_name = p.with_suffix('.pdf');

    if( not os.path.exists( os.path.join(dist_dir,pdf_file_name) ) ): # se il file PDF corrispondente non esiste crealo

        os.chdir(ROOT_PATH)
        os.chdir(dir_path)
        os.system("latexmk -pdf -f -output-directory="+ temp_dir +"  " + file_name)

        created_file_path = os.path.join(temp_dir,pdf_file_name)
        shutil.move(created_file_path,os.path.join(dist_dir,pdf_file_name))
        delete_auxiliary_files(temp_dir)

"""
Compila i file latex in .pdf spostandoli nella corretta cartella temp
in base al tipo di documento(interno/esterno, documento/verbale)
"""
def latex_to_pdf():
    src_walk = os.walk(SRC_PATH)
    for root,dirs,files in src_walk: # scorri la cartella /docs/src
        for folder in dirs:         # scorri cartelle in /docs/src
            if(folder != 'temp' and folder != 'assets'):   
                dir_listing = os.listdir(os.path.join(root,folder))
                for file_name in dir_listing:
                    file_path = (os.path.join(root,folder,file_name))
                    if os.path.isfile(file_path):
                        if( pathlib.Path(file_path).suffix == '.tex'):
                            compile_latex(os.path.join(root,folder),file_name)



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


























