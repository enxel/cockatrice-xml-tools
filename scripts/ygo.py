import urllib.request, json

req = urllib.request.Request(
    url="https://db.ygoprodeck.com/api/v7/cardsets.php", 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
sets = json.load(urllib.request.urlopen(req))

req = urllib.request.Request(
    url="https://db.ygoprodeck.com/api/v7/cardinfo.php",
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
cards = json.load(urllib.request.urlopen(req))

not_wanted = ["token","skill"]
not_monsters = ["spell","trap"]
not_pendulum = ["normal","effect","ritual","fusion","synchro","xyz","link"]
pendulum = [(lambda x: x+"_pendulum")(x) for x in not_pendulum]
link = ["link","link_pendulum"]
monsters = not_pendulum + pendulum
everyone = monsters + not_monsters

def format_cleanser(item):
    item = item.replace("<","&lt;")
    item = item.replace(">","&gt;")
    item = item.replace("&","&amp;")
    item = item.replace("\'","&apos;")
    item = item.replace("\"","&quot;")
    return item

f = open("Yu_Gi_Oh.xml","w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<cockatrice_carddatabase version=\"4\">\n")

f.write("\t<sets>\n")

for sset in sets:
    name = sset["set_code"]

    longname = format_cleanser(sset["set_name"])

    if "tcg_date" in sset:
        releasedate = sset["tcg_date"]
    else:
        releasedate = ""

    f.write(2*"\t"+"<set>\n")
    f.write(3*"\t"+"<name>"+name+"</name>\n")
    f.write(3*"\t"+"<longname>"+longname+"</longname>\n")
    f.write(3*"\t"+"<settype></settype>\n")
    f.write(3*"\t"+"<releasedate>"+releasedate+"</releasedate>\n")
    f.write(2*"\t"+"</set>\n")

f.write("\t</sets>\n")

f.write("\t<cards>\n")

for card in cards["data"]:
    maintype = card["frameType"]
    
    if maintype in everyone:
        name = format_cleanser(card["name"])

        text = ""

        if maintype in monsters:
            text += "Attribute: "+card["attribute"]+"\n\n"

        if maintype in pendulum:
            text += "Scale: "+str(card["scale"])+"\n\n"

        if maintype in link:
            text += "Link markers: "+" | ".join(card["linkmarkers"])+"\n\n"

        text += format_cleanser(card["desc"])+"\n\n"

        if "archetype" in card:
            text += "Archetype: "+format_cleanser(card["archetype"])+"\n\n"

        if maintype in monsters:
            if maintype in link:
                cmc = str(card["linkval"])
            else:
                cmc = str(card["level"])

        ttype = card["type"]+" - "+card["race"]

        if maintype in monsters:
            pt = str(card["atk"])
            if not(maintype in link):
                pt += "/"+str(card["def"])

        muid = str(card["id"])

        if maintype in not_monsters:
            tablerow = "0"
        else:
            if maintype in (link+pendulum):
                tablerow = "2"
            else:
                tablerow = "1"

        if "card_sets" in card:
            css = []
            for cs in card["card_sets"]:
                css.append((cs["set_code"],cs["set_rarity"]))

        picURL = card["card_images"][0]["image_url"]

        if "banlist_info" in card:
            format_tcg = "ban_tcg" in card["banlist_info"]
            format_goat = "ban_goat" in card["banlist_info"]
        else:
            format_tcg = False
            format_goat = False

        f.write(2*"\t"+"<card>\n")
        f.write(3*"\t"+"<name>"+name+"</name>\n")
        f.write(3*"\t"+"<text>"+text+"</text>\n")
        f.write(3*"\t"+"<prop>\n")
        f.write(4*"\t"+"<maintype>"+maintype+"</maintype>\n")
        f.write(4*"\t"+"<layout>normal</layout>\n")
        f.write(4*"\t"+"<manacost></manacost>\n")
        f.write(4*"\t"+"<side>front</side>\n")
        if maintype in monsters:
            f.write(4*"\t"+"<cmc>"+cmc+"</cmc>\n")
        else:
            f.write(4*"\t"+"<cmc></cmc>\n")
        f.write(4*"\t"+"<type>"+ttype+"</type>\n")
        if maintype in monsters:
            if maintype in link:
                f.write(4*"\t"+"<loyalty>"+pt+"</loyalty>\n")
            else:
                f.write(4*"\t"+"<pt>"+pt+"</pt>\n")
        if format_tcg:
            f.write(4*"\t"+"<format-tcg>Legal</format-tcg>\n")
        if format_goat:
            f.write(4*"\t"+"<format-goat>Legal</format-goat>\n")
        f.write(3*"\t"+"</prop>\n")
        if "card_sets" in card:
            for s in css:
                f.write(3*"\t"+"<set muid=\""+muid+"\" rarity=\""+s[1]+"\" picURL=\""+picURL+"\">"+s[0]+"</set>\n")
        else:
            f.write(3*"\t"+"<set muid=\""+muid+"\" picURL=\""+picURL+"\"></set>\n")
        f.write(3*"\t"+"<tablerow>"+tablerow+"</tablerow>\n")
        f.write(2*"\t"+"</card>\n")

f.write("\t</cards>\n")
f.write("</cockatrice_carddatabase>\n")
f.close()

print("It is done!")
