import re
from django.db import transaction

from . import parser_strategy as ps
from admin.models import StrutturaDatabase, Tabella, Campo
from admin import enums

class SQLParser(ps.ParserStrategy):
    
    def parse(self, uploaded_file):
        try:
        
            sql_script = uploaded_file.read().decode('utf-8')
            
            # Search for the "CREATE DATABASE IF NOT EXISTS" statement
            create_database_match = re.search(r'CREATE DATABASE IF NOT EXISTS (\w+)', sql_script)
            
            if not create_database_match:
                file_name = uploaded_file.name
                database_name = file_name.split('.')[0]  # Get name before the first dot
            else:
                database_name = create_database_match.group(1)
    
            if StrutturaDatabase.objects.filter(nome=database_name).exists():
                return enums.ParserStatus.DB_ALREADY_EXISTS, "Errore: esiste già una struttura con nome " + database_name

            with transaction.atomic():
                struttura_db = StrutturaDatabase.objects.create(
                    nome=database_name,
                    descrizione=""
                )
        
            # Extract table names and fields from SQL script
            table_fields = re.findall(r'CREATE TABLE IF NOT EXISTS (\w+) \((.*?)\);', sql_script, re.DOTALL)

            for table_name, fields in table_fields:
                fields = re.findall(r'(\w+) (\w+(?:\([\w,]+\))?).*?,', fields)
                with transaction.atomic():
                    tabella, _ = Tabella.objects.get_or_create(
                        nome=table_name,
                        descrizione="",
                        struttura=struttura_db
                    )
                for field_name, field_type in fields:
                    with transaction.atomic():
                        Campo.objects.create(
                            nome=field_name,
                            tipo=field_type,
                            tabella=tabella
                        )
        except Exception as e:
            return enums.ParserStatus.CREATION_DB_ERROR, "Errore nella creazione della struttura: " + str(e)       
        return enums.ParserStatus.SUCCESS, "Struttura creata con successo"