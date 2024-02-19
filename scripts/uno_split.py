import os
from PIL import Image

def crop(path, origin, height, width, k, m, area):
    im = Image.open(origin)
    imgwidth, imgheight = im.size
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            print(str(j)+" "+str(i)+" "+str(j+width)+" "+str(i+height))
            box = (j-(k%14), i-m, j-(k%14)+width, i-m+height)
            a = im.crop(box)
            #print("hola")
            try:
                #print("domo")
                o = a.crop(area)
                #print("meller")
                route = os.path.join(path,"IMG%s.png" % k)
                #print(route)
                o.save(route)
                #print("PUTA")
            except:
                print("chuare")
                pass
            k +=1
        m +=1

path = "H:/Cockatrice/data/pics/CUSTOM"
origin = "H:/Cockatrice/data/pics/CUSTOM/uno.png"

h = 215
w = 144

k = 0
m = 0
area = (0,0,w,h)

crop(path,origin,h,w,k,m,area)

print("LA SOCA")
