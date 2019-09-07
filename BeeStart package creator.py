from PIL import Image
from glob import glob
from zipfile import *
from json import *
from os import path
import sys

print("Welcome to the BeeStart package creator!")
print("")
print("This utility can help creating BeeStart packages, but it will work,")
print("like bee2.4, only with .jpg files")
print("this utility will overwrite the images you privide with resized ones")
print("make a backup of the images before run this\n")
workdir = input("paste here the path to folder with the images: ")#input folder
print("") 
nimg = len(glob(workdir+"/*.jpg"))
if (nimg==0):
    print("error! no images found!")
    print("Press return key to exit.")
    f = input("")
    sys.exit()
print("loading "+str(nimg)+" jpg images...")
for files in glob(workdir+"/*.jpg"):#resize to work size all images
    file, ext = path.splitext(files)
    im = Image.open(files)
    imr = im.resize((1366, 765))
    imr.save(file+".jpg", "JPEG")
    print("loaded resized "+file+".jpg into workdir")

"""here we create a dict for the info.json, with the author, the package name and later all the images"""
info = {"name": "","author": ""}#crate a new dictionary for the info.json
info["name"] = input("input package name: ")#apply the name of the package
info["author"] = input("input author: ")#apply the author of the package
print("setting up images in info.json.")

"""here we create a dictionary with all the images"""
images = {}#create a new dict for the images
for files in glob(workdir+"/*.jpg"):#re-get all images
    workfilel = list(files)  #convert to list
    i = 0
    while(not i>=len(workdir)):
        del(workfilel[0])    #delete the character 0
        i=i+1
    workfile = "".join(workfilel)  #convert back to string
    print("adding "+workfile+" to image list")
    images[len(images)] = workfile#add the current file to the dict
info["images"] = images#add the images dict to the info dict
print("creating info.json with this data:")
print(info)

"""here we create the actual json file"""
infojson=dumps(info)
with open('info.json', 'w') as json_file:
    dump(info, json_file)
print("created info.json!")

"""here we compress all the files in a zip"""
package_name = workdir+info["name"]+".zip"
with ZipFile(package_name, 'w') as myzip:
    myzip.write("info.json")
    print("compressed file: info.json")
    for files in glob(workdir+"/*.jpg"):#re-re-get all images
        myzip.write(files)
        print("compressed file: "+files)
print("DONE!")
print("package file created!")
print("you can found it on "+workdir)
print("\nPress return to exit")
f = input("")


