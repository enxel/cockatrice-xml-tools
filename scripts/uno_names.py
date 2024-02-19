
import os

path = "H:/Cockatrice/data/pics/CUSTOM/"
files = os.listdir(path)

colors = ["red","yellow","green","blue"]
contents = ["0","1","2","3","4","5","6","7","8","9","cancel","reverse","plus2"]

cont = 0
i = 0
j = 0
for file in files:
   cadena = str(file)
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

"""
      
      for i in range(0,4):
         for j in range(0,13):
   #newcadena = cadena.replace("%20"," ")
   #newcadena = cadena.replace(".full","")
   newcadena = cadena.replace(".jpg",".full.jpg")
   os.rename(path + cadena, path + newcadena)
"""
