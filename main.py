import flickrapi
import json
import urllib.request 
import sys
import argparse

api_key = u"2ec631c82f61982abba4248986dfe229"
api_secret = u"59251a851149a537"

# user_id = "26839719@N02" 
# photo_id = "8680500073"

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')

parser = argparse.ArgumentParser(
    prog="FlickrDownload",
    description="Simple script to download Flickr profile with metadata (photo description)."
)

parser.add_argument('-u', '--uid', type=str, default="")
parser.add_argument('-p', '--pid', type=str, default="")
parser.add_argument('-d', '--description', action="store_true")
args = parser.parse_args()

def get_uid(photo_id):
    return json.loads(flickr.photos.getInfo(photo_id=photo_id))["photo"]["tags"]["tag"][0]["author"]

def init(key, secret, uid="", pid=""):
    if uid:
        bulk_download(uid)
    elif pid:
        bulk_download(get_uid(pid))
    elif not pid and not uid:
        print("Seemes, you are have empty 'user_id field.\nTo get user id, enter id of any photo, made by user you want to download.'")
        while len(pid := input("--> ")) == 0:
            print("Please, enter valid photo id, you can get it in picture's URL address.\nExample: 8680500073\n")
        bulk_download(get_uid(pid))
    else:
        print("Please, enter user-id or picture-id of user, you want to download.")   

def bulk_download(uid):
    user = flickr.people.getPublicPhotos(user_id=uid, per_page=500)
    user = json.loads(user)

    if user["stat"] == "fail":
        print("API error:", user["message"])
        sys.exit()

    photos_count = user["photos"]['total']
    content = user["photos"]["photo"]

    for i in range(photos_count):
        id = content[i]["id"]
        title = content[i]["title"]
        server = content[i]["server"]
        secret = content[i]["secret"]

        url =  f"https://live.staticflickr.com/{server}/{id}_{secret}_b.jpg"
        
        print(f"{id} - {title} - {url}")
        
        # Downloading Photo with urllib function: https://docs.python.org/3/library/urllib.request.html#urllib.request.urlretrieve
        urllib.request.urlretrieve(url, title + ".jpg") 

        if args.description == True:
            metadata = json.loads(flickr.photos.getInfo(photo_id=id))
            
            description = metadata["photo"]["description"]["_content"]
            print(description)
        
            data = open(title + ".txt", "w")
            data.write(description)
            
            data.close()
            
if __name__ == "__main__":
    init(api_key, api_secret, args.uid, args.pid)