#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path

import fnmatch

from mutagen.mp3 import MP3
import mutagen.id3
from mutagen.easyid3 import EasyID3

def removeSpace(filename):
    id3info = MP3(filename,ID3=EasyID3)
    for k,vlist in id3info.items():
        for v in vlist:
            print v,"->",
            id3info[k]=v.strip()
            print id3info[k]
        id3info.save()

def pathDir(rootdir,dojob):
    for root,dirs,files in os.walk(rootdir):
        #for dirname in dirs:
        #    print unicode(dirname,'utf-8')
        for filename in files:
            if fnmatch.fnmatch(filename,"*.mp3"):
                fullpath=os.path.join(root,filename)
                print unicode(fullpath,'utf-8')
                dojob(fullpath)

def toUnicodeTag(filename):
    id3info = MP3(filename,ID3=EasyID3)
    for k,vlist in id3info.items():
        for v in vlist:
            print k,":",v
    
def main():
    #rootdir="/Users/irachex/Music/iTunes/iTunes Music/"
    rootdir="/Users/irachex/Desktop/1/"
    pathDir(rootdir,toUnicodeTag)
    #toUnicodeTag("1.mp3")
    
if __name__=="__main__":
    main()
