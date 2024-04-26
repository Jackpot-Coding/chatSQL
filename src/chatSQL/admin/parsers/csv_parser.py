import csv
import codecs
from django.db import transaction

from admin.models import StrutturaDatabase, Tabella, Campo
from admin import enums
from . import parser_strategy as ps

class CSVParser(ps.ParserStrategy):
    
    def parse(self, uploaded_file):
        
        try:
            reader = csv.DictReader(
                    codecs.iterdecode(uploaded_file,encoding='utf-8')
                )
            
            file_name = uploaded_file.name.split('.')[0]
    
            if StrutturaDatabase.objects.filter(nome=file_name).exists():
                return enums.ParserStatus.DB_ALREADY_EXISTS, "Errore: esiste già una struttura con nome " + file_name
        
            with transaction.atomic():
                struttura_db= StrutturaDatabase.objects.create(
                    nome=file_name,
                    descrizione=""
                )
                
            for row in reader:
                with transaction.atomic():                
                    
                    # Create Tabella instance related to StrutturaDatabase
                    tabella, _ = Tabella.objects.get_or_create(
                        nome=row.get('Tabella', ''),
                        descrizione=row.get('descrizione', ''),
                        sinonimi=row.get('sinonimi', ''),
                        struttura=struttura_db
                    )
                    
                    # Create Campo instance related to Tabella
                    Campo.objects.create(
                        nome=row.get('Campo', ''),
                        tipo=row.get('tipo', ''),
                        sinonimi=row.get('sinonimi', ''),
                        tabella=tabella
                    )
        except Exception as e: 
            return enums.ParserStatus.CREATION_DB_ERROR, "Errore nella creazione della struttura: " + str(e)
        return enums.ParserStatus.SUCCESS, "Struttura creata con successo"