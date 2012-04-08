#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import fnmatch
import json
import time
from mutagen.mp3 import MP3
import mutagen.id3
from mutagen.easyid3 import EasyID3
import codecs

from robot import DoubanRobot
from config import DB_API_KEY, DB_API_SECRET

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')


class mp3info:
    id3_list = None
    def __init__(self, path):
        if fnmatch.fnmatch(path,"*.mp3"):
            id3info = MP3(path,ID3=EasyID3)
            self.id3_list = [id3info,]
        else:
            self.id3_list = list()
            for root,dirs,files in os.walk(path):
                print root, "artist:", root.split("/")[-2], ",album:", root.split("/")[-1]
                for filename in files:
                    if fnmatch.fnmatch(filename,"*.mp3"):
                        fullpath=os.path.join(root,filename)
                        id3info = MP3(fullpath,ID3=EasyID3)
                        if not ("artist" in id3info) and not ("performer" in id3info):
                            id3info["artist"] = [unicode(root.split("/")[-1]).encode("utf-8"),]
                        if not ("album" in id3info):
                            id3info["album"] = [unicode(root.split("/")[-2]).encode("utf-8"),]
                        self.id3_list.append(id3info)
    
    def get_infos(self):
        return self.id3_list
    
    def show(self):
        for id3info in self.id3_list:
            for k,vlist in id3info.items():
                for v in vlist:
                    print k,":",v


class Robot(DoubanRobot):
    def get_music_id(self, artist, album):
        try:
            jsondata = self.get("/music/subjects",param={"q":u"%s %s" % (unicode(album), unicode(artist)), "alt":"json" }).read()
            data = json.loads(jsondata)
        except:
            #print jsondata
            print "error:", album, artist
            return {}
        
        #print data
        idlist = list()
        for entry in data["entry"]:
            try: 
                if entry["author"][0]["name"]["$t"] == artist and entry["title"]["$t"] == album:
                    idlist.append(entry["id"]["$t"])
            except:
                #print entry
                pass
        
        info = {"artist":artist, "album":album, "list":idlist}
        return info
        
    def getall_music_id(self, id3_list):
        music_list = list()
        fetched = dict()
        for id3info in id3_list:
            try: 
                album = id3info["album"][0]
                if "artist" in id3info:
                    artist = id3info["artist"][0]
                elif "performer" in id3info:
                    artist = id3info["performer"][0]
            except:
                print id3info
                continue
            key = "%s %s" % (album, artist)
            if key in fetched:
                continue
            fetched[key]=True
            info = self.get_music_id(artist, album)
            print "get:", artist, album
            if info:
                music_list.append(info)
            time.sleep(4)
        return music_list
    
    def collection(self, id, artist, status="listened"):
        template = codecs.open('collection.xml', 'r', 'utf-8')
        data = template.read()
        template.close()
        
        data = data.replace(u"{{status}}", status)
        data = data.replace(u"{{id}}", id)
        data = data.replace(u"{{artist}}", artist)
        
        response = self.post("/collection", data)
        if response.status == 201:
            return True
        return False
        

def main():
    #rootdir="/Users/irachex/Music/iTunes/iTunes Music/"
    rootdir="/Users/irachex/Music/iTunes/iTunes Music/"
    info = mp3info(rootdir)
   # info.show()
    
    robot = Robot("", "")
    #print robot.get_auth_url()
    #raw_input()
    #print robot.token_key, robot.token_secret
    #robot.get_access_token(robot.token_key, robot.token_secret)
    #print robot.token_key, robot.token_secret
    #print robot.get_current_user()
    
    music_list = robot.getall_music_id(info.get_infos())
    for music in music_list:
        artist = music["artist"]
        album = music["album"]
        album_list = music["list"]
        for album_id in album_list:
            print "mark:", artist, album,
            print robot.collection(album_id, artist)
            time.sleep(4)
    
    #toUnicodeTag("1.mp3")
    
if __name__=="__main__":
    main()
