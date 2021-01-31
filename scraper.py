# Scrap images from a Google Images
# Written by Rutuparn Pawar (InputBlackBoxOutput)
# Created 14 Nov 2020

import requests

import urllib3
http = urllib3.PoolManager()
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

from io import BytesIO
import PIL.Image as Image

from html.parser import HTMLParser
from html.entities import name2codepoint

import os, sys
from tqdm import tqdm
import string

#------------------------------------------------------------------------------------------------
class SrcExtractor(HTMLParser):
  src = []
  def handle_starttag(self, tag, attrs):
    if tag == "img":
      for each in attrs:
        if each[0] == "data-src":
          # print(each[1])
          self.src.append(each[1])
         
srcExtractor = SrcExtractor()

#------------------------------------------------------------------------------------------------
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    } 

#------------------------------------------------------------------------------------------------
def getImages(search, limit=30, outDir=None, addon=""):
	try:
		print("\033[96m"+ f"Keyword:{search}" +"\033[00m\n") 

		try:
			print("Creating directory...", end="")
			if outDir == None:
				os.mkdir(search)
			else:
				os.mkdir(f"{outDir}/{search}")
			print("Done")
		except FileExistsError:
			print("\nDirectory already exits")

		url = f"https://www.google.com/search?q={addon}{search}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjozNPH4J3rAhVUU30KHXRzDSoQ_AUoAXoECBEQAw&biw=1366&bih=625"       
		response = requests.request("GET", url, headers=headers)
		srcExtractor.feed(response.text)
		len_src = len(srcExtractor.src)

		count = 0
		for each_src in tqdm(srcExtractor.src[:limit], bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}'):
			response = http.request('GET', each_src)
			img_data = BytesIO(response.data)
			image = Image.open(img_data).convert("RGBA")

			if outDir == None:
				image.save(f"{search}/{count+1}.png")
			else:
				image.save(f"{outDir}/{search}/{count+1}.png")
			count+=1

		print(f"Downloaded {count}/{limit} images")

		srcExtractor.src = [] 
		print("\033[97m" + 70 * '-' + "\033[00m") 

	except:
		print("\033[31m"+ "Something went wrong!\nPlease check passed options" +"\033[00m")
		sys.exit()

#------------------------------------------------------------------------------------------------

with open("/content/drive/My Drive/Animal Images/classes.txt", 'r') as infile:
  data = infile.read().splitlines()
  
  for each in data:
    getImages(each, limit=-1, outDir="/content/drive/My Drive/Animal Images/")


# Using only 'chicken' as keyword returned cooked chiken images!
# getImages("chicken", limit=-1, outDir="/content/drive/My Drive/Animal Images/", addon="live")

#------------------------------------------------------------------------------------------------
#EOF