#!/usr/bin/python

from threading import Thread
import os, sys
import math
from gmap_utils import *
from proxy import request

import time
import random

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):

    start_x, start_y = bd_latlng2xy(zoom, lat_start, lon_start)
    stop_x, stop_y = bd_latlng2xy(zoom, lat_stop, lon_stop)
    
    start_x = int(start_x//256)
    start_y = int(start_y//256)
    stop_x = int(stop_x//256)
    stop_y = int(stop_y//256)
    
    print("x range", start_x, stop_x)
    print("y range", start_y, stop_y)   
    
    for i in range(start_x, stop_x, 400):
        end = 400 if (i + 400) <= stop_x else (stop_x - i)
        for x in range(i, i + end):
            ths = []
            t = FastThread(x, start_y, stop_y, zoom, satellite)
            ths.append(t)
            t.start()
        for t in ths:
            t.join()


class FastThread(Thread):
    def __init__(self, x, start_y, stop_y, zoom, satellite):
        super(FastThread, self).__init__()
        self.x = x
        self.start_y = start_y
        self.stop_y = stop_y
        self.zoom = zoom
        self.satellite = satellite
    
    def run(self):
        for y in range(self.start_y, self.stop_y):
            if satellite:
                download_satellite(self.x, y, self.zoom)
                download_tile(self.x, y, self.zoom, True)
            else:
                download_tile(self.x, y, self.zoom)


def download_tile(x, y, zoom, satellite=False):
    url = None
    filename = None
    folder = "road/" if satellite else "tile/"
    scaler = "" if satellite else "&scaler=1"
    # styles is roadmap when downloading satellite
    styles = "sl" if satellite else "pl"

    query = "qt=tile&x=%d&y=%d&z=%d&styles=%s%s&udt=20170927" % (x, y, zoom, styles, scaler)
    url = "http://online0.map.bdimg.com/onlinelabel/?" + query
    filename = query + ".png"

    download_file(url, filename, folder)


def download_satellite(x, y, zoom):
    url = None
    filename = None
    folder = "it/"

    path = "u=x=%d;y=%d;z=%d;v=009;type=sate&fm=46&udt=20170927" % (x, y, zoom)
    url = "http://shangetu0.map.bdimg.com/it/" + path
    filename = path.replace(";", ",") + ".jpg"

    return download_file(url, filename, folder)


def download_file(url, filename, folder=""):
    full_file_path = folder + filename
    if not os.path.exists(full_file_path):
        try:
            res = request('get', url)
        except Exception as e:
            print("--", filename, "->", e)
            return False
        
        if res.content.startswith(b"<html>"):
            print("-- forbidden", filename)
            return download_file(url, filename, folder)
        
        print("-- saving " + filename)
        
        f = open(full_file_path, 'wb')
        f.write(res.content)
        f.close()
        return True
    else:
        print("-- existed " + filename)
        return True
            

if __name__ == "__main__":
    
    # zoom = 11
 
 #108.919174,34.238897
 #108.925911,34.235972

#浙江
 #127.01253,28.710287
 #117.703498,32.815861

#中国
 #67.004285,54.847671
 #133.271348,16.419887

    lat_start, lon_start =  16.419887, 67.004285,
    lat_stop, lon_stop = 54.847671,133.271348,

    satellite = False
    for zoom in range(9, 14):
        download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite)
