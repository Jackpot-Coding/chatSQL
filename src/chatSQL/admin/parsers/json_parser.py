import json
from django.db import transaction

from . import parser_strategy as ps
from admin.models import StrutturaDatabase, Tabella, Campo
from admin import enums

class JSONParser(ps.ParserStrategy):
    
    def parser(self, uploaded_file):
        db = json.load(uploaded_file)
        db_name = db["database"].get('nome')
        try:
            if StrutturaDatabase.objects.filter(nome=db_name).exists():
                return enums.ParserStatus.DB_ALREADY_EXISTS, "Errore: esiste già una struttura con nome " + db_name
    
            with transaction.atomic():
                struttura_db= StrutturaDatabase.objects.create(
                    nome=db_name,
                    descrizione=db["database"].get('descrizione')
                )
            for tabella in db["database"].get('tabelle'):
                with transaction.atomic():
                    tabella_db, _ = Tabella.objects.get_or_create(
                        nome=tabella.get('nome'),
                        descrizione=tabella.get('descrizione'),
                        sinonimi=tabella.get('sinonimi'),
                        struttura=struttura_db
                    )
                    for campo in tabella.get('campi'):
                        Campo.objects.create(
                            nome=campo.get('nome'),
                            tipo=campo.get('tipo'),
                            sinonimi=campo.get('sinonimi'),
                            tabella=tabella_db
                        )
        except Exception as e:
            return enums.ParserStatus.CREATION_DB_ERROR, "Errore nella creazione della struttura: " + str(e)
        return enums.ParserStatus.SUCCESS, "Struttura creata con successo"