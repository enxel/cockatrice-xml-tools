import time
import urllib.request, json

base = "https://digimoncard.io/api-public/"
baseUrl = base + "getAllCards.php?sort=name&series=Digimon+Card+Game&sortdirection=asc"
#finalurl = baseUrl + urllib.parse.quote(' ')

#print(finalurl)

positions = {"Digi-Egg":"0","Tamer":"1","Digimon":"2","Option":"3"}

def urlpetition(url):
    req = urllib.request.Request(
        url=url,
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return json.load(urllib.request.urlopen(req))

def format_cleanser(item):
    if not(item == None):
        item = item.replace("<","&lt;")
        item = item.replace(">","&gt;")
        item = item.replace("&","&amp;")
        item = item.replace("\'","&apos;")
        item = item.replace("\"","&quot;")
    return item

cards = urlpetition(baseUrl)

#print(cards)
#print(len(cards))

f = open("DigimonCardGame.xml","w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<cockatrice_carddatabase version=\"4\">\n")

f.write("\t<cards>\n")

for card in cards:
    f.write("\t\t<card>\n")
    f.write("\t\t\t<name>"+format_cleanser(card["name"])+" ["+card["cardnumber"]+"]</name>\n")

    #print(base+"search.php?card="+card["cardnumber"])
    cardobj = urlpetition(base+"search.php?card="+card["cardnumber"])[0]
    #print(cardobj)

    text = ""
    if cardobj["evolution_cost"] != None and cardobj["evolution_cost"] != "":
        text = text + "Evolution Cost: " + str(cardobj["evolution_cost"])
    if cardobj["evolution_color"] != None and cardobj["evolution_color"] != "":
        text = text + "\nEvolution Color: " + cardobj["evolution_color"]
    if cardobj["evolution_level"] != None and cardobj["evolution_level"] != "":
        text = text + "\nEvolution Level: " + str(cardobj["evolution_level"])
    if cardobj["xros_req"] != "" and cardobj["xros_req"] != None:
        text = text + "\nXros Requirements: " + cardobj["xros_req"]
    if text != "":
        text = text + "\n\n"
    text = text + cardobj["main_effect"]
    if cardobj["source_effect"] != "" and cardobj["source_effect"] != None:
        text = text + "\n\nSource Effect:\n" + cardobj["source_effect"]
    if cardobj["alt_effect"] != "" and cardobj["alt_effect"] != None:
        text = text + "\n\nAlternative Effect: \n" + cardobj["alt_effect"]
    f.write("\t\t\t<text>"+format_cleanser(text)+"</text>\n")

    f.write("\t\t\t<prop>\n")
    f.write("\t\t\t\t<maintype>"+cardobj["type"]+"</maintype>\n")
    f.write("\t\t\t\t<layout>normal</layout>\n")
    f.write("\t\t\t\t<manacost></manacost>\n")
    f.write("\t\t\t\t<side>front</side>\n")
    f.write("\t\t\t\t<cmc>"+str(cardobj["play_cost"])+"</cmc>\n")
    if cardobj["dp"] != None and cardobj["dp"] != "":
        f.write("\t\t\t\t<pt>"+str(cardobj["dp"])+"</pt>\n")
    if cardobj["level"] != None and cardobj["level"] != "":
        f.write("\t\t\t\t<loyalty>"+str(cardobj["level"])+"</loyalty>\n")
    color = cardobj["color"]
    if cardobj["color2"] != None and cardobj["color2"] != "":
        color = color + "/" + cardobj["color2"]
    f.write("\t\t\t\t<colors>"+color+"</colors>\n")
    type = ""
    if cardobj["digi_type"] != None and cardobj["digi_type"] != "":
        type = type + "-" + cardobj["digi_type"]
    if cardobj["digi_type2"] != None and cardobj["digi_type2"] != "":
        type = type + "-" + cardobj["digi_type2"]
    if cardobj["form"] != None and cardobj["form"] != "":
        type = type + "-" + cardobj["form"]
    if cardobj["attribute"] != None and cardobj["attribute"] != "":
        type = type + "-" + cardobj["attribute"]
    if cardobj["stage"] != None and cardobj["stage"] != "":
        type = type + "-" + cardobj["stage"]
    if type != "":
        f.write("\t\t\t\t<type>"+type+"</type>\n")
    f.write("\t\t\t</prop>\n")

    picurl = "https://world.digimoncard.com/images/cardlist/card/"+card["cardnumber"]+".png"
    f.write("\t\t\t<set muid=\""+str(cardobj["tcgplayer_id"])+"\" rarity=\""+cardobj["rarity"]+"\" picURL=\""+picurl+"\">"+card["cardnumber"]+"</set>\n")

    f.write("\t\t\t<tablerow>"+positions[cardobj["type"]]+"</tablerow>\n")

    f.write("\t\t</card>\n")
    
    time.sleep(0.75)

f.write("\t</cards>\n")
f.write("</cockatrice_carddatabase>\n")
f.close()

print("It is done!")
