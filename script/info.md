# Script di compilazione dei file PDF da file Latex

Lo script genera i file PDF a partire dai file .tex presenti nella cartella `/doc/src`

Per eseguire lo script eseguire `/script/main.py`.

È necessario avere installato il pacchetto `latexmk`, normalmente presente nelle distribuzioni Latex per i vari sistemi operativi.

__*Se i file PDF sono già presenti questi non vengono sovrascritti.*__

Potrebbe essere necessario premere <kbd>Invio &crarr;</kbd> quando si presenta il testo

```
! Undefined control sequence.
l.61 \textcolor
{}{\rule{\textwidth}{5pt}}
?
```

a riga di comando