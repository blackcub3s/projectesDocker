


# 0. Índex

TO DO

# 1. Introducció

Aquest repositori conté diversos projectes desplegats dins de contenidors

# 2. Instal·lació docker

DIns la carpeta [instalacioDocker] mostro un arxiu en bash .sh amb el qual hauria de ser possible instal·lar automàticament docker al vostre sistema basat en linux (sempre que feu servir la shell bash). L'arxiu m'ha funcionat per a una distribució de linuxmint. Un cop estigui instal·lat podeu provar els projectes desplegats:

https://github.com/blackcub3s/projectesDocker/blob/5470b0485e9feb8026d3cfd3dc5c02bcd0a52bb3/instalacioDocker/instalaDocker.sh#L5-L34

# 3. ScrapEnsenyament

Dins de la carpeta [scrapEnsenyament](/scrapEnsenyament/) podem trobar l'script parsejaDifCob.py que pren una llista de URLs on hi ha diversos pdfs online amb ofertes laborals d'una borsa de professorat, que es van actualitzant periòdicament. En aquests llistats volem cercar grups de paraules (en aquest cas especialitats docents de les quals ens pugui interessar fer un seguiment).

Per fer això el programa descarrega els pdfs, obté el seu text pla i cerca els grups de paraules dins dels text pla de cada PDF. Per cada PDF informarà pel canal estàndard de sortida si existeixen ofertes laborals i, en breus, mitjançant notificació "push" s¡avisarà al mòbil de forma periòdica de les ofertes que van sortint:

https://github.com/blackcub3s/projectesDocker/blob/29f9aa18c99577194c8d3424dd491a2a01e2f704/scrapEnsenyament/parsejaDifCob.py#L3-L110

Ens interessa que aquest programa corri dins d'un entorn compartimentat, on ja hi hagi totes les dependències instalades (no només python 3 sino també els mòduls no pertanyents a llibreria estàndar tals com PyPDF2 (que passa PDF a text pla) o pytz (que permet controlar les hores mostrades de forma que es mostri l'hora espanyola sempre en tot moment). El servidor que el contingui probablement no tindrà aquestes dependències i de ben segur tampoc tindrem accés als permisos necessaris per poder instalar el que necessitem. Per tal de fer això una màquina virtual potser serviria però consumiria molts recursos, ja que requereix un sistema operatiu propi i emulació del hardware, que no necessitem. Només necessitem tenir les dependències instal·lades i l'accés al kernel del sistema operatiu. Això és justament el que fa docker: és un sistema de contenidors, compartimentat com una màquina virtual però molt més ràpid en execució, menys consumidor de memòria ram i d'espai (recursos que no sobren en servidors en recursos compartits). 

Abans de crear un contenidor docker amb la nostra app haurem de crear una nova imatge personalitzada amb el seu propi sistema d'arxius (amb l'script/S del nostre programa i les dependències instalades que aquest necessiti). Per fer-ho escriurem i executarem un fitxer <strong>dockerfile</strong> que contindrà les instruccions per tal de crear aquesta nova imatge: 

- 1. la imatge base de la qual partirem per crear la imatge nova (la base serà la imatge de python3, vegeu comanda FROM).
- 2. El directori de treball que serà l'arrel del contenidor que derivi de la imatge on s'executaran les comandes (vegeu comanda WORKDIR).
- 3. He instal·lat les dependències amb la comanda RUN (idealment millor anidar-les amb un && en comptes de fer diverses comandes RUN per tenir més eficiència).
- 4. He copiat del meu sistema a dins el directori de la imatge personalitzada el codi que necssita estar dins el sistema d'arxius de la nova imatge.
- 5. He escrit la comanda per defecte que es correrà en executar un contenidor derivat de la nova imatge que ens generarà el dockerfile en ser executat.

El dockerfile ha quedat, doncs, així:

https://github.com/blackcub3s/projectesDocker/blob/eecf579692d80f43d7c0b74788aa486d176b97a2/scrapEnsenyament/Dockerfile#L1-L14


Per executar-lo ho farem amb la comanda <strong>build</strong>, seguida de la etiqueta -t que ens permetrà donar el nom que nosaltres volguem a la imatge que volguem, i acabat amb . o ./ que ens permetrà executar el dockerfile des de la carpeta o directori on posem la comanda. Així doncs, nosaltres creem una image anomenada "scrapensenyament" amb la següent comanda:

```
docker build -t scrapensenyament ./
```

Per veure que hem creat aquesta imatge correctament podem comprovar-ho fent servir la comanda `docker images`:

![Ep! imatge no carregada.](/scrapEnsenyament/img/1_dockerBuild_creacioImatge.png)

Un cop tinguem la imatge construida podem fer servir aquesta imatge per tal de crear un contenidor o els que volguem (que idealment podrem desplegar en un servidor directmaent sempre que siguin de kernel linux i tinguin soport de docker, si hem creat la imatge en alguna distribució de linux). Aquest contenidor executarà automàticament el programa un cop arranqui.

Per crear el contenidor podrem fer-ho fent ```docker run -it scrapensenyament``` (que el crea i l'activa a partir de la imatge scrapensenyament que acabem de crear) o en dos passos (amb create i després amb start). En fer servir create, la sintaxis serà ```docker create scrapensenyament```. En aquest cas tenim la flag o opció ```--name``` que ens permetrà donar un nom al contenidor (perque el nom no sigui aleatori) així que li donarem de nom "contenidor_scrap_ensenyament" amb la següent comanda:

```
docker create --name contenidor_scrap_ensenyament scrapensenyament
```
Després d'haver creat el contenidor farem servir la sintaxi ```docker start contenidor_scrap_ensenyament```que en aquest cas podrem enriquir amb la flag -a per redirigir per pantalla la sortida del contenidor (que serà el print per pantalla del programa [parsejaDifCob.py](/scrapEnsenyament/parsejaDifCob.py)):

```
docker start -a contenidor_scrap_ensenyament
```

Podem veure el resultat de les dues comandes anteriors en la següent imatge:

![imatge start i create no ha carregat](/scrapEnsenyament/img/startIcreate_demo.PNG)

NOTA: No considero recomanable abuscar da la comanda de docker ```run``` perquè cada cop que l'utilitzem estem creant un nou contenidor i corrent-lo, no estem executant un contenidor que ja està creat. En canvi, si fem servir la comanda ```start`` sempre estem utilitzant un conductor ja existent (que crearem només un sol cop amb create).

NOTA 2: Si el contenidor tingués també entrada de l'usuari haruiem de fer servir la flag -i en fer start perquè puguem interactuar amb ell: (docker start -ai contenidor_scrap_ensenyament).

La sortida per pantalla del programa és la següent:

```
execució script --> [ 02/06/2024 || 20:51h ]
difCob Lleida.pdf descarregat correctament!
difCob Tarragona.pdf descarregat correctament!
difCob Girona.pdf descarregat correctament!
difCob BaixLlob_CREDA_CFA.pdf descarregat correctament!
difCob VallesOccidental.pdf descarregat correctament!
difCob aran.pdf descarregat correctament!
difCob CatalunyaCentral.pdf descarregat correctament!
------------------------------

 -- cerca en --> [difCob Lleida.pdf]
        No s'han trobat especialitats, per ara, en aquest document

------------------------------

 -- cerca en --> [difCob Tarragona.pdf]
        No s'han trobat especialitats, per ara, en aquest document

------------------------------

 -- cerca en --> [difCob Girona.pdf]
        No s'han trobat especialitats, per ara, en aquest document

------------------------------

 -- cerca en --> [difCob BaixLlob_CREDA_CFA.pdf]
        No s'han trobat especialitats, per ara, en aquest document

------------------------------

 -- cerca en --> [difCob VallesOccidental.pdf]
        [[[ AN ]]]      AN-29/05 (1)  AN-Anglès                                             TERMINI OBERT 

------------------------------

 -- cerca en --> [difCob aran.pdf]
        No s'han trobat especialitats, per ara, en aquest document

------------------------------

 -- cerca ESPECÍFICA en --> [difCob CatalunyaCentral.pdf]
        No s'han trobat especialitats, per ara, en aquest document 
```

# 3. to do
