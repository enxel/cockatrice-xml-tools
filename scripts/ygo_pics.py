import urllib.request, json

req = urllib.request.Request(
    url="https://db.ygoprodeck.com/api/v7/cardinfo.php",
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
cards = json.load(urllib.request.urlopen(req))

def patch_name(name):
    banned = "#%&{}\\<>*?/$!\'\":@+`|="
    new_name = ""
    for c in name:
        if c in banned:
            new_name += ""
        else:
            new_name += c
    return new_name

f = open("ygo_pics.csv","w")
f.write("name,url\n")
for card in cards["data"]:
    f.write(patch_name(card["name"])+","+card["card_images"][0]["image_url"]+"\n")
f.close()

print("It is done!")
