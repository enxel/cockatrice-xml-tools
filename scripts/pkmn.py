from pokemontcgsdk import Card
from pokemontcgsdk import Set
cards = Card.all()
sets = Set.all()

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
  "Colorless": "{C}"
}

def format_cleanser(item):
    if not(item == None):
        item = item.replace("<","&lt;")
        item = item.replace(">","&gt;")
        item = item.replace("&","&amp;")
        item = item.replace("\'","&apos;")
        item = item.replace("\"","&quot;")
    return item

f = open("PokemonTCG.xml","w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<cockatrice_carddatabase version=\"4\">\n")

f.write("\t<sets>\n")

for sset in sets:
    name = format_cleanser(sset.id.upper())

    longname = format_cleanser(sset.name)

    settype = format_cleanser(sset.series)

    releasedate = sset.releaseDate
    releasedate = releasedate.replace("/","-")

    f.write(2*"\t"+"<set>\n")
    f.write(3*"\t"+"<name>"+name+"</name>\n")
    f.write(3*"\t"+"<longname>"+longname+"</longname>\n")
    f.write(3*"\t"+"<settype>"+settype+"</settype>\n")
    f.write(3*"\t"+"<releasedate>"+releasedate+"</releasedate>\n")
    f.write(2*"\t"+"</set>\n")

f.write("\t</sets>\n")

f.write("\t<cards>\n")

for card in cards:
    name = format_cleanser(card.name)
    
    text = ""

    if not(card.evolvesFrom == None):
        text += "Evolves from: " + card.evolvesFrom + "\n\n"
        
    if not(card.ancientTrait == None):
        at = card.ancientTrait
        text += "Ancient Trait: " + at.name + "\n" + at.text + "\n\n"
        
    if not(card.abilities == None):
        for a in card.abilities:
            text += a.type + " - " + a.name + "\n" + a.text + "\n\n"

    if not(card.attacks == None):
        for a in card.attacks:
            for e in a.cost:
                text += cost_dict[e]
            if not(a.text == None):
                text += "  " + a.name + "  " + str(a.damage) + "\n" + a.text + "\n\n"
            else:
                text += "  " + a.name + "  " + str(a.damage) + "\n\n"

    if not(card.rules == None):
        text += "Special rules:\n"
        for r in card.rules:
            text += r + "\n"
        text += "\n"

    text += "Weakness:\n"
    if not(card.weaknesses == None):
        for w in card.weaknesses:
            text += cost_dict[w.type] + ": " + w.value + "\n"
    text += "\n"

    text += "Resistance:\n"
    if not(card.resistances == None):
        for r in card.resistances:
            text += cost_dict[r.type] + ": " + r.value + "\n"
    text += "\n"

    text += "Retreat cost: "
    if not(card.retreatCost == None):
        for e in card.retreatCost:
            text += cost_dict[e]
    text += "\n"

    if not(card.flavorText == None):
        text += "--------\n" + card.flavorText + "\n\n"

    maintype = card.supertype

    ttype = ""
    if not(card.subtypes == None):
        ttype += " / ".join(card.subtypes)

    if not(card.types == None):
        colors = ""
        for c in card.types:
            colors += cost_dict[c]

    text = format_cleanser(text)

    loyalty = card.hp

    cmc = card.convertedRetreatCost

    format_unlimited = card.legalities.unlimited
    format_expanded = card.legalities.expanded
    format_standard = card.legalities.standard

    rarity = format_cleanser(card.rarity)

    muid = format_cleanser(card.id)

    picURL = card.images.large

    num = card.number

    setCode = format_cleanser(card.set.id.upper())

    if card.supertype == "Pokémon":
        tablerow = 0
    else:
        if card.supertype == "Trainer" and not(card.subtypes == None) and "Stadium" in card.subtypes:
            tablerow = 3
        else:
            tablerow = 2

    if not(card.subtypes == None) and ("LEGEND" in card.subtypes or "BREAK" in card.subtypes):
        cipt = 1
    else:
        cipt = None

    f.write(2*"\t"+"<card>\n")
    f.write(3*"\t"+"<name>"+name+" ["+setCode+"]</name>\n")
    f.write(3*"\t"+"<text>"+text+"</text>\n")
    f.write(3*"\t"+"<prop>\n")
    f.write(4*"\t"+"<maintype>"+maintype+"</maintype>\n")
    f.write(4*"\t"+"<layout>normal</layout>\n")
    f.write(4*"\t"+"<manacost></manacost>\n")
    f.write(4*"\t"+"<side>front</side>\n")
    f.write(4*"\t"+"<cmc>"+str(cmc)+"</cmc>\n")
    f.write(4*"\t"+"<type>"+ttype+"</type>\n")
    if not(card.types == None):
        f.write(4*"\t"+"<colors>"+colors+"</colors>\n")
    f.write(4*"\t"+"<loyalty>"+str(loyalty)+"</loyalty>\n")
    if not(format_unlimited == None):
        f.write(4*"\t"+"<format-unlimited>Legal</format-unlimited>\n")
    if not(format_expanded == None):
        f.write(4*"\t"+"<format-expanded>Legal</format-expanded>\n")
    if not(format_standard == None):
        f.write(4*"\t"+"<format-standard>Legal</format-standard>\n")
    f.write(3*"\t"+"</prop>\n")
    if rarity == None:
        f.write(3*"\t"+"<set muid=\""+muid+"\" picURL=\""+picURL+"\" num=\""+str(num)+"\">"+setCode+"</set>\n")
    else:
        f.write(3*"\t"+"<set rarity=\""+rarity+"\" muid=\""+muid+"\" picURL=\""+picURL+"\" num=\""+str(num)+"\">"+setCode+"</set>\n")
    f.write(3*"\t"+"<tablerow>"+str(tablerow)+"</tablerow>\n")
    if not(cipt == None):
        f.write(3*"\t"+"<cipt>"+str(cipt)+"</cipt>\n")
    f.write(2*"\t"+"</card>\n")

f.write("\t</cards>\n")
f.write("</cockatrice_carddatabase>\n")
f.close()

print("It is done!")
