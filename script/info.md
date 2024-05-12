# Script di compilazione dei file PDF da file Latex

Lo script genera i file PDF a partire dai file .tex presenti nella cartella `/doc/src`

Per eseguire lo script eseguire `/script/main.py`.

È necessario avere installato il pacchetto `latexmk`, normalmente presente nelle distribuzioni Latex per i vari sistemi operativi, e i pacchetti `Jinja2`, `requests` e `dotenv`. 

Aggiungere il proprio token GitHub [generato qui](https://github.com/settings/tokens) ad il file locale `.env` con chiave `GH_TOKEN`.

__*Se i file PDF sono già presenti e aggiornati questi non vengono sovrascritti.*__

Potrebbe essere necessario premere <kbd>Invio &crarr;</kbd> quando si presenta il testo

```
! Undefined control sequence.
l.61 \textcolor
{}{\rule{\textwidth}{5pt}}
?
```

a riga di comando