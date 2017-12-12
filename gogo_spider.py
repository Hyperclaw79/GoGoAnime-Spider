import bs4
from bs4 import BeautifulSoup
import requests
import html
import time
        
def fetcher(url):
   response = requests.get(url)
   sauce = response.content
   soup = bs4.BeautifulSoup(sauce,"lxml")
   links = soup.body.find_all('a')
   for link in links:
       if "vidstream" in str(link) and "download" in str(link):
           s = str(link)
           dl = s.split('"')[1]
           dl = html.unescape(dl)
           return dl
       else:
           pass
        
def downloader(urlc,i,qual):
   if urlc == None:
      print('Episode %d is not out yet.' % i)
      return "Stop"
   else:
      s = ""
      if qual == "Any":
          response = requests.get(urlc)
          sauce = response.content
          soup = bs4.BeautifulSoup(sauce,"lxml")
          s = "http:"+soup.find('iframe')['src']
      else:  
          dl = fetcher(urlc)
          response = requests.get(dl)
          sauce = response.content
          soup = bs4.BeautifulSoup(sauce,"lxml")
          links = soup.body.find_all('a')
          hrefs=[]
          for link in links:
             hrefs.append(str(link).split('href="')[1].split('>')[0])
          link_qual = [link for link in hrefs if qual in link]
          if len(link_qual) == 0:
             print("Didn't find any link with mentioned quality.\n")
             link_480 = [link for link in links if "480P" in str(link)]
             if len(link_480) != 0:
                print("Fetching 480P instead.\n")
                s = link_480[0]
             else:
                link_360 = [link for link in links if "360P" in str(link)]
                if len(link_480) != 0:
                   print("Fetching 360P instead.\n")
                   s = link_360[0]
                else:
                   print("Didn't find a direct link. Skipping this episode.")
          else:
             s = link_qual[0]
      try:   
         li = html.unescape(s).replace('"','')
         hook = li.split("title=")[1]
         alt = hook.replace("(",'').replace(" - mp4)",'-').replace(" ",'-')
         li = li.replace(hook,alt)
         with open('Links2.txt','a') as f:
            f.write(li+"\n\n")
         with open('Links.txt','a') as f:
            f.write("\n\nEpisode No. "+str(i)+":\n"+li)
         print("Episode No. "+str(i)+": "+li)
      except Exception as e:
         print(str(e))        

def searcher(name):
   searchlink = "https://ww3.gogoanime.io/search.html?keyword=" + name.replace(" ","%20")
   response = requests.get(searchlink)
   sauce = response.content
   soup = bs4.BeautifulSoup(sauce,"lxml")
   listing = soup.find_all('ul',{'class':'items'})
   if 'category' not in str(listing):
      print("No such anime found.\n")
      time.sleep(0.5)
      return invoker()
   links = listing[0].find_all('a')
   shows = []
   for link in links:
       title = str(link).split('category/')[1].split('"')[0]
       if title not in shows:
           shows.append(title)
   print('\nList of all the available anime:\n')
   i = 1
   for show in shows:
       print(str(i)+". "+show+"\n")
       i = i+1
   choice = input('Enter the corresponding number to choose the anime:\n')
   return shows[int(choice)-1]

def invoker():
   anime = searcher(input("Enter the name of the anime you wish to download:\n"))
   return anime
url = "https://ww3.gogoanime.io/{}-episode-1".format(invoker())
with open('Links2.txt','w') as f:
   f.write("")
with open('Links.txt','w') as f:
   f.write("")
num = int(input('Enter the number of episodes:\n'))
while True:
   mode = input('Choose the quality:\n1. 360p\n2. 480p\n3. 720p\n4. Any\n')
   if int(mode) == 1:
      qual = "360P"
      break
   elif int(mode) == 2:
      qual = "480P"
      break
   elif int(mode) == 3:
      qual = "720P"
      break
   elif int(mode) == 4:
      qual = "Any"
      break     
   else:
       print('Please choose 1, 2 or 3.')

for i in range(num):
    urlc = url.replace("1",str(i+1),1)
    flag = downloader(urlc,i+1,qual)
    if flag == "Stop":
       continue
