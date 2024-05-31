FROM python:3

#especifiquem directori de treball on hi haurà l'arrel de l'aplicació
WORKDIR /usr/src/app 

# PyPDF2p permet parsejar un pdf a text i pytz permet manejar bé les zones temporals
# ja que en docker no apareix bé el temps a l'hora espanyola
RUN pip install PyPDF2 && pip install pytz

#copiem l'script a l'arrel de la imatge
COPY parsejaDifCob.py /usr/src/app/

# comanda per defecte que s'executarà a l'arrancar el contenidor instanciat a partir de la imatge
CMD [ "python", "./parsejaDifCob.py" ]