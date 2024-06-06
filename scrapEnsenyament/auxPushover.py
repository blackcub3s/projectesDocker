import http.client, urllib.parse





def enviarNotificacio_Pushover(stringNotificacio):
	"""TO DO: ENVIA NOTIFICACIO DE QUE EL PROGRAMA HA ESTAT INICIAT"""
	print("---------------------------------")
	print("-Enviant notificació a pushover!-")
	print("---------------------------------")

	conn = http.client.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	  urllib.parse.urlencode({
	    "token": "aes2y22jowd1rugucho5ifknd5tge2",  #TOKEN CORRESPONENT a l'app anomenada scrapEnsenyament en el servei de notificacions pushover
	    "user": "us2o7tz49v2dbbyp9j8raq6r1m5q1m",   #USUARI DE PUSHOVER --> aquesta clau n'hi ha una per cada usuari (en aquest cas la meva)
	    "message": stringNotificacio,
	  }), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()
	print("------------------------------")
	print("-Notificació a pushover feta!-")
	print("------------------------------")
    



if __name__ == "__main__":
    s = "hola!"
    enviarNotificacio_Pushover(s)