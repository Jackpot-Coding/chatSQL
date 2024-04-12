# Istruzioni per il testing

## Strumenti

- Prospector - analisi statica del codice
  
- Django Tests - test dinamici
  
- Coverage - test coverage
  

## Installazione

`pip install prospector`

`pip install coverage`

## Come fare

Per lanciare i test statici lanciare dalla cartella `src/chatSQL`

`prospector` : da info sull'analisi statica del codice

`coverage run --source='.' manage.py test`per lanciare i test ed il loro coverage

se i test sono superati: `coverage report` per vedere il report di coverage

## Test di GitHub

Ad ogni push si attiva una GitHub action automatica che lancia le operazioni sopra definite e compare una spunta verde o una x rossa in base al superamento o meno dei test.

## Impostazioni prospector

Le impostazioni di prospector possono essere trovare nel file `src/chatSQL/prospector.yaml`