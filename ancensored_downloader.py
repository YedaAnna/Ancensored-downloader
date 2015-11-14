# @filename: ancensored_downloder.py
# @usage: python ancensored_downloader.py *url to image gallery*
# @author: YedaAnna
# @description: Downloads images from ancensored.com
# @version: 1.0
# @date: Wednesday 3rd November 2015
import os
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time
import sys
import re
import random
import datetime

global base_link, site_link, url
start = time.time()
site_link = "http://ancensored.com/"
url = newurl = []

if len(sys.argv) > 2:
    base_link = sys.argv[1]
    folder_name = sys.argv[2]
    subfolder_name = str(datetime.date.today())
else:
    base_link = sys.argv[1]
    parsed = urllib.parse.urlparse(sys.argv[1])
    folder_name = parsed.path.split('/')[3]
    subfolder_name = parsed.path.split('/')[2]


def list_images():
    global name, url, img, nextpage_link, newlist, newurl, thumbnail
    base_contents = urllib.request.urlopen(base_link).read()
    parsed_html = BeautifulSoup(base_contents)
    img = parsed_html.find_all(src=re.compile("jpg"))
    url = []
    newurl = []
    for link in img:
        url.append(link.get('src'))
    avoidthumbnails()


def avoidthumbnails():
    global size, newurl
    for i in range(len(url)):
        try:
            size = urllib.request.urlopen(url[i]).info()['Content-Length']
        except ValueError as e:
            print(e)
    if int(size) < 50000:  # if size is <50kb it is a thumbnail
        fullimages()
    else:
        newurl = url
        download_images()


def fullimages():
    global newurl
    newurl = []
    for i in range(len(url)):
        thumbnaail_url_split = urllib.parse.urlparse(url[i])
        if "vthumbs" in thumbnaail_url_split.path.split('/'):
            thumbnail = os.path.splitext(url[i])[0]
            newurl.append(thumbnail + '_full.jpg')
        elif "gallery_thumb" in thumbnaail_url_split.path.split('/'):
            thumbnail_split_array = []
            thumbnail_split_array = thumbnaail_url_split.path.split('/')
            thumbnail_split_array.pop(4)
            thumbnail_split_array.pop(4)
            thumbnail = '/'.join(thumbnail_split_array)
            newurl.append(site_link + thumbnail)
        else:
            continue
    download_images()


def download_images():
    for i in range(len(newurl)):
        try:
            urllib.request.urlretrieve(
                newurl[i], folder_name + str(random.randrange(1000)) + ".jpg")
        except urllib.error.URLError as e:
            print(e.reason)

if not os.path.exists(os.getcwd() + '/' + folder_name + '/' + subfolder_name):
    os.makedirs(os.getcwd() + '/' + folder_name + '/' + subfolder_name)
os.chdir(os.getcwd() + '/' + folder_name + '/' + subfolder_name)
list_images()
print("End of Program :)")
print("Time taken: " + str(time.time() - start) + " seconds")
