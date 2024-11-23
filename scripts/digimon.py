import urllib.request, json

baseUrl = "https://digimoncard.io/api-public/getAllCards.php?sort=name&series=Digimon+Card+Game&sortdirection=asc"
#finalurl = baseUrl + urllib.parse.quote(' ')

#print(finalurl)

req = urllib.request.Request(
    url=baseUrl,
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
cards = json.load(urllib.request.urlopen(req))

#print(cards)

f = open("DigimonCardGame.xml","w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<cockatrice_carddatabase version=\"4\">\n")

f.write("\t<cards>\n")

for card in cards:
    f.write("\t\t<card>\n")
    f.write("\t\t\t<name>"+card["name"]+" ["+card["cardnumber"]+"]</name>\n")
    picurl = "https://world.digimoncard.com/images/cardlist/card/"+card["cardnumber"]+".png"
    f.write("\t\t\t<set picURL=\""+picurl+"\">"+card["cardnumber"]+"</set>\n")
    f.write("\t\t</card>\n")

f.write("\t</cards>\n")
f.write("</cockatrice_carddatabase>\n")
f.close()

print("It is done!")
#muid=\""+card["cardnumber"]+"\" 