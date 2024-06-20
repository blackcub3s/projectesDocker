


# 0. Índex

TO DO

# 1. Introducció

Aquest repositori conté diversos projectes desplegats dins de contenidors

# 2. Instal·lació docker

DIns la carpeta [instalacioDocker] mostro un arxiu en bash .sh amb el qual hauria de ser possible instal·lar automàticament docker al vostre sistema basat en linux (sempre que feu servir la shell bash). L'arxiu m'ha funcionat per a una distribució de linuxmint. Un cop estigui instal·lat podeu provar els projectes desplegats:

https://github.com/blackcub3s/projectesDocker/blob/5470b0485e9feb8026d3cfd3dc5c02bcd0a52bb3/instalacioDocker/instalaDocker.sh#L5-L34

# 3. ScrapEnsenyament

# 3.1 Crear la imatge docker i executar un contenidor en local

Dins de la carpeta [scrapEnsenyament](/scrapEnsenyament/) podem trobar l'script parsejaDifCob.py que pren una llista de URLs on hi ha diversos pdfs online amb ofertes laborals d'una borsa de professorat, que es van actualitzant periòdicament. En aquests llistats volem cercar grups de paraules (en aquest cas especialitats docents de les quals ens pugui interessar fer un seguiment).

Per fer això el programa descarrega els pdfs, obté el seu text pla i cerca els grups de paraules dins dels text pla de cada PDF. Per cada PDF informarà pel canal estàndard de sortida si existeixen ofertes laborals i també enviarà una notificació "push" al meu mòbil de forma periòdica de les ofertes que van sortint.

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

# 3.2. Moure la imatge al registry d'azure i crear un contenindor al núvol

## Pas 1: instalar 

Per tal de poder tenir el contenidor de la nostra app funcionant en remot podem pujar la imatge a alguna de les arquitectures serverless disponibles: podem triar AWS o Azure, per exemple. Triem azure perquè té un plan de 100$ anuals en cas que siguis estudiant (a diferència d'AWS).

Per tal de fer-ho hem de pujar la imatge a l'`azure container registry` o ACS. Un cop la tinguem allà dins el propi núvol podrem crear un contenidor que derivi d'aquesta imatge. 

Per poder accedir al servei d'azure caldrà que instalem la command line interface d'Azure (la `azure cli`). Podem fer-ho seguint les instruccions de la [pàgina oficial](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt):

## PAS1: Instalem la cli amb el sistema precompilat pels desenvolupadors de microsoft (en aquest cas, una opció més senzilla que fer-ho amb el gestor de paquets apt)

```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## PAS 2: Iniciem la sessió

```
az login 

```
Amb la comanda anterior ens redirigirà a l'aplicació web per iniciar sessió, que en el meu cas la confirmació per la terminal es veurà així:

Vegeu imatge: [capturaAzureLogin.png](/scrapEnsenyament/img/capturaAzureLogin.png)

Per veure que s'ha creat correctament podem fer `az account show` i obtiundrem la informació del nostre compte en format JSON:

```
{
  "environmentName": "AzureCloud",
  "homeTenantId": "DADA PRIVADA",
  "id": "DADA PRIVADA",
  "isDefault": true,
  "managedByTenants": [],
  "name": "Azure for Students",
  "state": "Enabled",
  "tenantDefaultDomain": "edu.gva.es",
  "tenantDisplayName": "Conselleria d'Educació",
  "tenantId": "73dd1114-ef7d-40c7-8669-569d32e7e29b",
  "user": {
    "name": "EL_MEU_CORREU_PRIVAT@alu.edu.gva.es",
    "type": "user"
  }
}

```

Acte seguit creem un grup. Cal especificar la localització i el nom del "resource-group", que serà com una espècie de col·lecció lògica de recursos que es gestiona com una sola entitat:

``` 
az group create --location westeurope --resource-group scrapEnsenyament

```

Si s'ha creat bé obtindrem una sortida per pantalla en format JSON  que identificarà el grup que acabem de crear (que també la podrem obtenir, després de crear el grup, fent `az group list` ):

```
{
  "id": "/subscriptions/UNCODINOCOPIAT/resourceGroups/scrapEnsenyament",
  "location": "westeurope",
  "managedBy": null,
  "name": "scrapEnsenyament",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}

```
Ara podem afegir una etiqueta al grup (no es obligatori però es una bona pràctica fer-ho):

```
az group update --name scrapEnsenyament --set tags.entorn=provesScrapEnsenyament

```
Si la comanda anterior s'ha executat correctament, en fer de nou `az group list` hauriem de veure que la clau "tags" dins del json imprès pel canal estàndard de sortida haruaid'haver canviat de null a "entorn":"provesScrapEnsenyament" així:

```
{
  "id": "/subscriptions/UNCODINOCOPIAT/resourceGroups/scrapEnsenyament",
  "location": "westeurope",
  "managedBy": null,
  "name": "scrapEnsenyament",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": {
    "entorn": "provesScrapEnsenyament"
  },
  "type": "Microsoft.Resources/resourceGroups"
}

```
## PAS 3: Connectem al azure container registry (el registre d'imatges d'azure o ACR)

Per fer-ho tenim la següent comanda:

```
az acr login --name blackcub3s

``` 

## PAS 4: Etiquetem la imatge localment en docker per fer-la apta per a pujar-la al registre d'imatges d'Azure

Caldrà especificar el servidor d'inici de sessió amb la següent sintaxi a la terminal:

```
docker tag <local_image_name>:<tag> <acr_login_server>/<repository_name>:<tag>
```
Per trobar el servidor de login d'ACR anirem a portal.azure.com i clicarem en el link al nostre repositori:

[imatge a repo acr no ha carregat!](/scrapEnsenyament/img/azure20jun_A.png)

I aleshores en consultarem l'acr_login_server:

[imatge a servidor de login d'acr!](/scrapEnsenyament/img/azure20jun_B.png)

I per tant ara ja podem etiquetar la imatge "scrapensenyament" per poder-la pujar després a ACR és la següent. Per a fer-ho hem de indicar amb docker tah seguit de dos arguments: el primer, el nom de la imatge actual i la seva etiqueta (<nom_imatge>:<etiqueta>); i el segon el nom que tindrà l'alies de la imatge referenciada al primer argument, reflexant, entenc, els directoris interns del registry d'azure donats per: ` <acr_login_server>/<repository_name>/<image_name>:<tag> `. Per al nostre cas serà:

```
docker tag scrapensenyament:latest blackcub3s.azurecr.io/blackcub3s/scrapensenyament:latest
```

Comprovem que s'ha creat l'alies de la imatge etiquetada tal i com ho requereix azure, fent servir la comanda `docker images` i observem que la primera lína conté l'alies a la imatge:

[imatge sobre alies d'imatge reetiquetada per azure no ha carregat!](/scrapEnsenyament/img/azure20jun_C.png)

## PAS 5: Pujem la imatge al ACR mitjançant la subcomanda push de docker

Ara que ja hem etiquetat la imatge per a que pugui emmagatzemar-se al container registry d'azure pujem la imatge reetiquetada amb la comanda push (simplement agafem el nom que hem reetiquetat, que serà el nom de l'alies de la imatge creada en l'apartat anterior seguit de l'etiqueta "latest"):

```
docker push blackcub3s.azurecr.io/blackcub3s/scraensenyament:latest
```
En fer això ens apareixerà la següent pantalla de pujada si ho hem fet bé (en aquest cas la imatge pesa 1 GB i tardarà en pujar-se):

[imatge sobre la pujada a ACR de la imatge!](/scrapEnsenyament/img/azure20jun_D.png)

I quan acabi ens sortirà el següent missatge en la terminal, sense errors:

[imatge sobre la pujada a ACR de la imatge!](/scrapEnsenyament/img/azure20jun_E.png)

I podrem veure que la imatge s'ha pujat mirant a les estadístiques del nostre repositori:

[imatge de la imatge docker pujada no carregada](/scrapEnsenyament/img/azure20jun_F.png)



EN RESUM, els passos per pujar la imatge de docker del nostre linux a l'ACR o registre de contenidors d'azure serà:

1. Iniciar sessió (*login*): Autentiqueu-vos amb el vostre registre de contenidors d'Azure.
2. Etiquetar: (*tag*) Etiqueteu la vostra imatge local amb el nom del servidor d'inici de sessió de l'ACR i el repositori.
3. Pujar (*push*): Pugeu la imatge etiquetada a l'ACR.


## PAS 6: Creació de contenidor a partir de la imatge pujada a ACR fent servir kubernetes

  TO DO
  
# 4. to do
