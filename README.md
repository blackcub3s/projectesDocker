

# 0. Índex

# 1. Introducció

# 2.ScrapEnsenyament

Dins de la carpeta [scrapEnsenyament](/scrapEnsenyament/) podem trobar l'script parsejaDifCob.py que pren una llista de URLs on hi ha diversos pdfs online amb ofertes laborals, que es van actualitzant periòdicament, en els quals volem cercar grups de paraules (en aquest cas especialitats docents de les quals ens pugui interessar fer un seguiment).

Per fer això el programa descarrega els pdfs, obté el seu text pla i cerca els grups de paraules. Per cada PDF informarà per pantalla si existeixen ofertes laborals i, en breus, mitjançant notificació "push" se m'avisarà al mòbil de forma periòdica de les ofertes que van sortint:

https://github.com/blackcub3s/projectesDocker/blob/29f9aa18c99577194c8d3424dd491a2a01e2f704/scrapEnsenyament/parsejaDifCob.py#L3-L110

Ens interessa que aquest programa corri dins d'un entorn compartimentat, on ja hi hagi totes les dependències instalades (no només python 3 sino també els mòduls no pertanyents a llibreria estàndar tals com PyPDF2 (que passa PDF a text pla) o pytz (que permet controlar les hores mostrades de forma que es mostri l'hora espanyola sempre en tot moment). El servidor que el contingui probablement no tindrà aquest es dependències i de ben segur tampoc tindrem accés als permisos necessaris per poder instalar el que necessitem. Per tal de fer això una màquina virtual potser serviria però consumiria molts recursos: no necessitem el nostre propi sistema operatiu, només es necessiten les dependències i l'accés al kernel del sistema operatiu. Per solucionar-ho tenim docker: un sistema de contenidors, també compartimentat com una màquina virtual però molt més ràpid en execució, menys consumidor de memòria ram i d'espai (coses que no sobre en els servidors que tenen recursos compartits). 

Abans de crear un contenidor docker haurem de crear primer una imatge amb el seu propi sistema d'arxius (amb el nostre programa i les dependències instalades). Per fer-ho he creat el següent dockerfile:

https://github.com/blackcub3s/projectesDocker/blob/29f9aa18c99577194c8d3424dd491a2a01e2f704/scrapEnsenyament/parsejaDifCob.py#L3-L14

Per tal de crear la imatge necessitem executar el següent dockerfile:

https://github.com/blackcub3s/projectesDocker/blob/eecf579692d80f43d7c0b74788aa486d176b97a2/scrapEnsenyament/Dockerfile#L1-L14


Per executar-lo ho farem amb la comanda build, seguida de la etiqueta -t que ens permetrà donar el nom que nosaltres volguem a la imatge (scrapensenyament) i seguit de . o de ./ que ens permetrà executar el dockerfile si correm la comanda a la mateixa carpeta on estigui:

```
docker build -t scrapensenyament ./
```

D'aquesta manera creem la imatge i podem veure que aquesta existeix fent servir la comanda `docker images`:

![imatge no carregda](/scrapEnsenyament/img/1_dockerBuild_creacioImatge.png)

Un cop tenim la imatge construida podem fer servir aquesta imatge per tal de crear un contenidor que executi el programa un cop s'arranqui. Així doncs creem el contenidor. Podem fer-ho fent docker run -it scrapensenyament (que el crea i l'activa) o en dos passos (amb create i després amb start). En fer servir create la sintaxis es ```docker create nom_imatge```. En aquest cas tenim la flag o opció --name que ens permet donar un nom al contenidor (perque el nom no sigui aleatori) així que fem:

```
docker create --name contenidor_scrap_ensenyament scrap_ensenyament
``
I després fem servir la sintaxi ```docker start nom_contenidor```que en aquest podem enriquir amb la flag -a per redirigir per pantalla la sortida del contenidor (que serà el print per pantalla del programa [parsejaDifCob.py](/scrapEnsenyament/parsejaDifCob.py)):

```
docker start -a contenidor_scrap_ensenyament
```

Podem veure el resultat de les dues comandes anteriors en la següent imatge:

![imatge start i create no ha carregat](/scrapEnsenyament/img/startIcreate_demo.PNG)

NOTA: No considero recomanable abuscar da la comanda de docker ```run``` perquè cada cop que l'utilitzem estem creant un nou contenidor i corrent-lo, no estem executant un contenidor que ja està creat. En canvi, si fem servir la comanda ```start`` sempre estem utilitzant un conductor ja existent (que crearem només un sol cop amb create).



# 3. to do
