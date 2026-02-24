import time
from tqdm import tqdm
from tcgdexsdk import TCGdex, Language

print("Libraries imported")

cost_dict = {
  "Grass": "{G}",
  "Fire": "{F}",
  "Water": "{W}",
  "Lightning": "{L}",
  "Psychic": "{P}",
  "Fighting": "{Fi}",
  "Darkness": "{Dk}",
  "Metal": "{M}",
  "Fairy": "{Fy}",
  "Dragon": "{D}",
  "Colorless": "{C}",
  "Free": "   "
}

def format_cleanser(item):
    if not(item == None):
        item = item.replace("<","&lt;")
        item = item.replace(">","&gt;")
        item = item.replace("&","&amp;")
        item = item.replace("\'","&apos;")
        item = item.replace("\"","&quot;")
    return item

print("Configuring data source...")
tcgdex = TCGdex(Language.EN)
print("Data source configured")

print("Requesting data...")
cards = tcgdex.card.listSync()
sets = tcgdex.set.listSync()
print(f"Data obtained:\n   - {len(cards)} cards obtained\n   - {len(sets)} sets obtained")

f = open("PokemonTCG.xml","w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<cockatrice_carddatabase version=\"4\">\n")

f.write("\t<sets>\n")

print("Writing set data...")
for sset in tqdm(sets):
    fsset = tcgdex.set.getSync(sset.id)

    name = format_cleanser(fsset.id.upper())

    longname = format_cleanser(fsset.name)

    settype = format_cleanser(fsset.serie.name)

    releasedate = fsset.releaseDate

    f.write(2*"\t"+"<set>\n")
    f.write(3*"\t"+"<name>"+name+"</name>\n")
    f.write(3*"\t"+"<longname>"+longname+"</longname>\n")
    f.write(3*"\t"+"<settype>"+settype+"</settype>\n")
    f.write(3*"\t"+"<releasedate>"+releasedate+"</releasedate>\n")
    f.write(2*"\t"+"</set>\n")

    time.sleep(0.2)

f.write("\t</sets>\n")

print("Set data written")

f.write("\t<cards>\n")

print("Writing card data...")
for rcard in tqdm(cards):
    if rcard.id == "exu-%3F":
        continue
    
    card = tcgdex.card.getSync(rcard.id)

    name = format_cleanser(card.name)
    
    text = ""

    if not(card.evolveFrom == None):
        text += "Evolves from: " + card.evolveFrom + "\n\n"
        
    if not(card.abilities == None):
        for a in card.abilities:
            text += a.type
            if not(a.name == None):
                text += " - " + a.name + "\n"
            else:
                text += "\n\n"
            if not(a.effect == None):
                text += a.effect + "\n\n"

    if not(card.attacks == None):
        for a in card.attacks:
            if not(a.cost == None):
                for e in a.cost:
                    text += cost_dict[e]
            if not(a.effect == None): 
                text += "  " + a.name
            text += "  " + str(a.damage) + "\n"
            if not(a.effect == None):
                text += a.effect + "\n\n"

    text += "Retreat cost: "
    if not(card.retreat == None):
        text += str(card.retreat)
    text += "\n"

    maintype = card.category

    if not(card.types == None):
        colors = ""
        for c in card.types:
            colors += cost_dict[c]

    text = format_cleanser(text)

    loyalty = card.hp

    format_standard = card.legal.standard
    format_expanded = card.legal.expanded

    rarity = format_cleanser(card.rarity)

    muid = format_cleanser(card.id)

    if not(card.image == None):
        picURL = card.image + "/high.png"
    else:
        picURL = ""

    num = card.localId

    setCode = format_cleanser(card.set.id.upper())

    if maintype == "Pokémon":
        tablerow = 0
    else:
        if maintype == "Trainer":
            tablerow = 3
        else:
            tablerow = 2

    f.write(2*"\t"+"<card>\n")
    f.write(3*"\t"+"<name>"+name+" ["+muid.upper()+"]</name>\n")
    f.write(3*"\t"+"<text>"+text+"</text>\n")
    f.write(3*"\t"+"<prop>\n")
    f.write(4*"\t"+"<maintype>"+maintype+"</maintype>\n")
    f.write(4*"\t"+"<layout>normal</layout>\n")
    f.write(4*"\t"+"<manacost></manacost>\n")
    f.write(4*"\t"+"<side>front</side>\n")
    f.write(4*"\t"+"<cmc></cmc>\n")
    f.write(4*"\t"+"<type></type>\n")
    if not(card.types == None):
        f.write(4*"\t"+"<colors>"+colors+"</colors>\n")
    f.write(4*"\t"+"<loyalty>"+str(loyalty)+"</loyalty>\n")
    if not(format_standard == None):
        f.write(4*"\t"+"<format-standard>Legal</format-standard>\n")
    if not(format_expanded == None):
        f.write(4*"\t"+"<format-expanded>Legal</format-expanded>\n")
    f.write(3*"\t"+"</prop>\n")
    if rarity == None:
        f.write(3*"\t"+"<set muid=\""+muid+"\" picURL=\""+picURL+"\" num=\""+str(num)+"\">"+setCode+"</set>\n")
    else:
        f.write(3*"\t"+"<set rarity=\""+rarity+"\" muid=\""+muid+"\" picURL=\""+picURL+"\" num=\""+str(num)+"\">"+setCode+"</set>\n")
    f.write(3*"\t"+"<tablerow>"+str(tablerow)+"</tablerow>\n")
    f.write(2*"\t"+"</card>\n")

    time.sleep(0.2)
    
f.write("\t</cards>\n")

print("Card data written")

f.write("</cockatrice_carddatabase>\n")
f.close()

print("It is done!")
