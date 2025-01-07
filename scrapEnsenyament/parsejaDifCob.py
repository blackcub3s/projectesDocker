#!/usr/bin/python3

import urllib.request
from datetime import datetime
import os
import PyPDF2
import pytz
from auxPushover import enviarNotificacio_Pushover


s = '' #on posaré l'string de la notificació

# COMPUTO L'HORA A ESPANYA (EL CONTENIDOR TÉ UNA HORA DIFERENT) i l'imprimeixo per pantalla. IIndispensable usar pytz
def imprimeix_hora_espanyola():
    global s 

    current_time = str(datetime.now(pytz.timezone("Europe/Madrid")))  #per escollir timezone fas pytz.all_timezones
    dia, hora = current_time.split()
    dia, hora = dia.split("-"), hora.split(":")
    dia.reverse()

    missatge = "execució script --> [ "+dia[0]+"/"+dia[1]+"/"+dia[2]+" || "+hora[0]+":"+hora[1]+"h ]"
    s = s + missatge + "\n"
    print(missatge)


#FUNCIO FETA PER XAT GPT
def pdf_to_text(file_path):
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except PyPDF2.errors.PdfReadError:
        return "errorPdfAtext"



#FUNCIO FETA PER XAT GPT: 
def descarregaPdf(url, nomArxiu):
    try:
        # Open the URL
        with urllib.request.urlopen(url) as response:
            # Read the PDF content
            pdf_content = response.read()
            
            # Save the PDF content to a file
            with open(nomArxiu, 'wb') as f:
                f.write(pdf_content)
        print(nomArxiu+" descarregat correctament!")
    except Exception as e:
        print(f"Error descarregant pdf: {e}")




#PRE: llista_dpcuments es una llista de tuples amb dos valors: nom del fitxer que vols guardar i ubicacio
#      descsarregals: boolea que, si es true, torna a descarregar els fitxers a cada execució del programa. En cas contrari no es descarrega.
#POST: els documents pdf de llista_documents queden descarregats d'ensenyament al directori on s'executa l'script si descarregals es True.
def guardaPdfs(llista_documents, descarregals):
    if descarregals:
        for document in llista_documents:
            nomDoc, urlDoc = document[0], document[1]
            descarregaPdf(urlDoc, nomDoc)
    else:
        print("\nFitxers NO actualitzats")

# PRE: una llista d'especialiitats i una llista de tuples on primer element
#      tupla es nom del pdf a cercar. Els pdfs de la tupla han d'existir al directori on s'executa el programa.
# POST: S'imprimeix cada linia que té una ocurrència de qualsevol dels elements
#      (especialitats) de ll_esp (llista especialitats)-
def fesScrapDocuments(ll_esp, ll_docs):
    global s 

    for doc in ll_docs:
        print("------------------------------\n")

        s = s + " -- cerca en --> ["+doc[0]+"]"+"\n"
        print(" -- cerca en --> ["+doc[0]+"]")
        
        textPDF = pdf_to_text(doc[0]) 
        if textPDF == "errorPdfAtext":
            s = s + "\t----- ################################################# ------\n\t----- ### ERROR DE TRANSCRIPCIÓ EN AQUEST DOCUMENT! ### ------\n\t----- ################################################# ------\n"
            print("\t----- ################################################# ------\n\t----- ### ERROR DE TRANSCRIPCIÓ EN AQUEST DOCUMENT! ### ------\n\t----- ################################################# ------\n")            
        else:
            ll_linies_PDF = textPDF.split("\n")
            trobat = False
            for i in range(len(ll_linies_PDF)):
                for especialitat in ll_esp:
                    if especialitat in ll_linies_PDF[i]:
                        s = s + "\t[[[ "+especialitat+ " ]]]\t"+ll_linies_PDF[i] + "\n"
                        print("\t[[[ "+especialitat+ " ]]]\t"+ll_linies_PDF[i])
                        trobat = True
            if not trobat:
                s = s + "\tNo s'han trobat especialitats, per ara, en aquest document"+"\n"
                print("\tNo s'han trobat especialitats, per ara, en aquest document")
            print("")
    
#PRE: una llista d'especialitats de la qual prendras els noms dels pdfs de la primera columna
#POST: pdfs esborrats de la carpeta
def esborra_pdfs(ll_esp, carregatPdfs):
    if carregatPdfs:
        for pdf, url in ll_esp:
            os.remove(pdf)
        
        
#PRE:    ll_esp: la llista espeicalitats | cataluyaCentral: una tupla amb dos valors (el nom del pdf de la cat central i la seva url
#       cal que existeixi el pdf de la catalunya central al directori de treball.
#POST:  Impressio de si hi ha o no especialitats a la catalunyacentral i quines, si n'hi ha

#FUNCIONAMENT: Es una funció especial que lllegeix el document de la catalunya central que
#       és únic i requereix adaptar-s'hi. Llegeix perfecte al menys per a un nombre de documents no nul. també guarda en la variable
#       global s l'string que anira a la notificaicó mobil via pushover
def fesScrapCatalunyaCentral(ll_esp, catalunyaCentral):
    global s
    print("------------------------------\n")

    s = s + " -- cerca ESPECÍFICA en --> ["+catalunyaCentral[0]+"]"+"\n"
    print(" -- cerca ESPECÍFICA en --> ["+catalunyaCentral[0]+"]")

    textPDF = pdf_to_text(catalunyaCentral[0]) 
    ll_linies_PDF = textPDF.split("\n")

    i = 0
    trobat = False
    while i < len(ll_linies_PDF):
        linia = ll_linies_PDF[i]
        try:
            if linia.index("Especialitat") == 0:
                for esp in ll_esp:
                    if esp in ll_linies_PDF[i+1].split()[0]:
                        s = s + "\t[[[ "+esp+ " ]]]\t" + ll_linies_PDF[i+1] + "\n"
                        print("\t[[[ "+esp+ " ]]]\t" + ll_linies_PDF[i+1])
                        trobat = True
                
                i = i + 1 #salto la linia seguent perque no te sentit mirar una linia que ja se que no conte el grup Especialitat
        except ValueError:
            xuclaSeguentLinia = False
        
        i = i + 1

    if not trobat:
        s = s + "\tNo s'han trobat especialitats, per ara, en el pdf de la catalunya central" + "\n\n"
        print("\tNo s'han trobat especialitats, per ara, en el pdf de la catalunya central")
    print("")


    



if __name__ == "__main__":
    #MOSTRO L'HORA EN QUE S'HA EXECUTAT L'SCRIPT
    imprimeix_hora_espanyola()

    #LLISTA DE TUPLES (nom amb que guardaré el document, url d'on fem scrap del document)
    llista_documents = [("difCob Lleida.pdf","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/lleida/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/LLE-SEC-dificil-cobertura-oferta-vacants.pdf"),
                        ("difCob terresDeLebre.pdf", "https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/terres-ebre/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/TEB-SEC-dificil-cobertura-oferta-vacants.pdf"), #ok 07.01
                        ("difCob baixLLobregat.pdf", "https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/baix-llobregat/personal-docent/nomenaments-telematics/dificil-cobertura/serveis-educatius/PENDENTS_BLL-Serveis-Educatius-dificil-cobertura-oferta-vacants.pdf"),
                        ("difCob Tarragona.pdf","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/tarragona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/TAR-SEC-dificil-cobertura-oferta-vacants.pdf"),
                        ("difCob Girona.pdf","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/girona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/GIR-SEC-dificil-cobertura-oferta-vacants.pdf"),
                        ("difCob VallesOccidental.pdf","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/valles-occidental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/VOC-SEC-dificil-cobertura-oferta-vacants.pdf"), 
                        ("difCob aran.pdf","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/alt-pirineu-aran/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/APA-SEC-dificil-cobertura-oferta-vacants.pdf")]
    
    #EL PDF DE LA CATALUNYA CENTRAL ES MOLT DIFERENT I CAL TRACTAR-LO A PART
    catalunyaCentral = ("difCob CatalunyaCentral.pdf","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/catalunya-central/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/CCE-SEC-dificil-cobertura-oferta-vacants.pdf")
    

    #especialitats buscades als PDFs
    especialitats = ["AN","PSI","627","SCS"]
    

    # si poso true actualitza els documents en temps real, sino tira dels que has descarregat prèviament (NO ELS GUARDA)
    guardaPdfs(llista_documents+[catalunyaCentral], True)  
    fesScrapDocuments(especialitats, llista_documents)
    fesScrapCatalunyaCentral(especialitats, catalunyaCentral)
    esborra_pdfs(llista_documents+[catalunyaCentral],True); #per evitar vestigis me'ls carrego un cop llegits (Si es true, si es false no fa res)
    enviarNotificacio_Pushover(s) #s es l'string de la notificacio (si vols evitar que s'envii comenta aquesta linia)