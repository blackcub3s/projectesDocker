#!/bin/bash

#genero la IMATGE scrapensenyament a partir del dockerfile de la carpeta anidada scrapEnsenyament.
docker build -t scrapensenyament ./scrapEnsenyament

#per si el contenidor derivat de la IMATGE funcionava, el paro. 
#Si existeix l'he d'esborrar (nomes ho puc fer si esta parat).
docker stop contScrapEns
docker rm contScrapEns

#creo contenidor contScrapEns des de la imatge scrapensenyament recent creada.
#redirecciono port 8000 (dreta dels dospunts) al port XXXX (esquerra dels dos punts)
docker create -p 8000:8000 --name contScrapEns scrapensenyament 
docker start -a contScrapEns #redirigeixo la sortida per veure errors
