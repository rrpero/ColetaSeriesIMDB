from bs4 import BeautifulSoup
import requests
import csv

#lista de series definida manuamente
linksSeries = [
["Game Of Thrones","tt0944947"],
["Breaking Bad","tt0903747"],
["Rick and Morty","tt2861424"],
["The Wire","tt0306414"],
["Avatar: The Last Airbender","tt0417299"],
["The Sopranos","tt0141842"],
["Sherlock","tt1475582"],
["Fargo","tt2802850"],
["True Detective","tt2356777"],
["Death Note","tt0877057"],
["Firefly","tt0303461"],
["Stranger Things","tt4574334"],
["Black Mirror","tt2085059"],
["Friends","tt0108778"],
["Seinfeld","tt0098904"],
["Attack on Titan","tt2560140"],
["Peaky Blinders","tt2442560"],
["House of Cards","tt1856010"],
["Westworld","tt0475784"]
]

table = [["Temporada","Ep. Nome","Ep. N.","Nota","Série"]]
#line=

for linkSerie in linksSeries:

	#conecta no link de uma temporada pra listar todas temporadas
	page2 = requests.get("https://www.imdb.com/title/"+linkSerie[1]+"/episodes/_ajax?season=1")
	#print(page.content)

	soup2 = BeautifulSoup(page2.content, 'html.parser')

	mydivs2 = soup2.find("select", {"id": ["bySeason"]}).findAll("option")


	#para cada temporada
	for div2 in  mydivs2:

		print("https://www.imdb.com/title/"+linkSerie[1]+"/episodes/_ajax?season="+div2.get_text().replace('\n', ' ').replace('\r', '').replace(' ', ''))
		page = requests.get("https://www.imdb.com/title/"+linkSerie[1]+"/episodes/_ajax?season="+div2.get_text().replace('\n', ' ').replace('\r', '').replace(' ', ''))
		#page = requests.get("https://www.imdb.com/title/tt0411008/episodes/_ajax?season=2")
		soup = BeautifulSoup(page.content, 'html.parser')
		
		#pega items de cada episódio
		mydivs = soup.findAll("div", {"class": ["list_item odd", "list_item even"]})
		
		teveZero = False
		for div in mydivs:
			episodio = int(div.find("meta")['content'])
			if episodio == 0:
				teveZero = True
			
			if teveZero:
				episodio = int(div.find("meta")['content'])+1
			line=[]
			line.append(int(div2.get_text().replace('\n', ' ').replace('\r', '').replace(' ', '')))
			line.append(div.find("strong").get_text())
			#print(div.find("strong").get_text())
			#line.append(div.find("meta")['content'])
			#print(div.find("meta")['content'])
			line.append(episodio)
			print(episodio)
			try:
				line.append(float(div.find("span", {"class": ["ipl-rating-star__rating"]}).get_text()))
				line.append(linkSerie[0])			
				table.append(line)
			except AttributeError:
				#algumas temporadas ou episodios sao pré-listados e nao  tem nota
				print ("Não tem nota")
			
			
			print(line)

		#break
with open('series.csv', 'w') as output_file:

	writer = csv.writer(output_file, dialect='excel',delimiter=';',lineterminator='\n')
	
	for dat in table:
		line = []
		writer.writerow(dat)

	output_file.close()
