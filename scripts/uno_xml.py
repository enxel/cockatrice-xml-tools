import os

path = "H:/Cockatrice/data/pics/CUSTOM/"
files = os.listdir(path)

xml = open('UNO.xml','w')

xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
xml.write("<cockatrice_carddatabase version=\"4\">\n")
xml.write("\t<sets>\n")
xml.write("\t\t<set>\n")
xml.write("\t\t\t<name>UNO</name>\n")
xml.write("\t\t\t<longname>The game ideal to lose friends.</longname>\n")
xml.write("\t\t\t<settype>Custom</settype>\n")
xml.write("\t\t\t<releasedate>Hace un vergo :^)</releasedate>\n")
xml.write("\t\t</set>\n")
xml.write("\t</sets>\n")
xml.write("\t<cards>\n")

cont = 1
for file in files:
   cadena = str(file)
   card = cadena.replace(".png","")
   if not(cadena == "UNO.xml") and not(cadena == "xml.py") and not(cadena == "names.py") and not(cadena == "spliy.py") and not(cadena == "uno.png"):
      xml.write("\t\t<card>\n")
      xml.write("\t\t\t<name>"+card+"</name>\n")
      xml.write("\t\t\t<text>Just play it, dude!</text>\n")
      xml.write("\t\t\t<prop>\n")
      xml.write("\t\t\t\t<layout>normal</layout>\n")
      xml.write("\t\t\t\t<side>front</side>\n")
      xml.write("\t\t\t\t<type> </type>\n")
      xml.write("\t\t\t\t<maintype> </maintype>\n")
      xml.write("\t\t\t\t<manacost> </manacost>\n")
      xml.write("\t\t\t\t<cmc>0</cmc>\n")
      xml.write("\t\t\t\t<format-legacy>legal</format-legacy>\n")
      xml.write("\t\t\t</prop>\n")
      xml.write("\t\t\t<set uuid=\""+str(cont)+"\" muid=\""+str(cont)+"\">UNO</set>\n")
      xml.write("\t\t\t<related> </related>\n")
      xml.write("\t\t\t<tablerow>2</tablerow>\n")
      xml.write("\t\t</card>\n")
      cont += 1

print(cont-1)
      
xml.write("\t</cards>\n")
xml.write("</cockatrice_carddatabase>\n")
xml.write("")

xml.close()


"""
cont = 0
i = 0
j = 0
for file in files:
   
   print(cadena)
   if not(cadena == "IMG13.png") and not(cadena == "IMG69.png") and not(cadena == "names.py") and not(cadena == "spliy.py") and not(cadena == "uno.png"):
      newcadena = colors[i] + "_" + contents[j] + ".png"
      print(newcadena)
      os.rename(path + cadena, path + newcadena)
      if j == 12:
         j = 0
         i += 1
      else:
         j += 1
      cont += 1
print(cont)
      
      for i in range(0,4):
         for j in range(0,13):
   #newcadena = cadena.replace("%20"," ")
   #newcadena = cadena.replace(".full","")
   newcadena = cadena.replace(".jpg",".full.jpg")
   os.rename(path + cadena, path + newcadena)
"""
