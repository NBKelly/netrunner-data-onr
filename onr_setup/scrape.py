## pre-requisites: requests_html, bs4
## what does this do?
##  fetches all the data on ONR cards from the emergency shutdown website
##  this fetches the data for all three sets, and returns a dict {} for each card
##  this can later be transformed into useful data for ONR cards on jinteki

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

def replace(str):
    if str == "Leland, Corportate Bodyguard":
        return "Leland, Corporate Bodyguard"
    return str

URL = "https://www.emergencyshutdown.net/webminster/sets/"
SETS = ["base", "proteus", "classic"]

for SET in SETS:
    C_URL = URL+SET

    session = HTMLSession()
    page = session.get(C_URL)
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    boxes = soup.find_all('div', class_='panel panel-primary')
    for box in boxes:
        dict = {}
        card_title = box.find(class_='panel-heading').text.strip()
        #print(card_title)
        dict['title'] = replace(card_title)
        
        card_image_url = box.find(class_="onr_img")['src']        
        #print(card_image_url)
        dict['image'] = card_image_url
        dict['set'] = SET
        
        sub = box.find(class_="col-md-offset-1 col-md-7")
        titles = sub.find_all("span", id="title")
        labels = sub.find_all("label")

        for index in range(0, len(titles)):
            title = titles[index].text.strip()
            label = re.sub('[^A-Za-z0-9]+', '', labels[index].text.strip().lower())
            dict[label] = title

        print(dict)
#        for title in titles:
#            print(title.text.strip())

            
#        print(sub[3])
        
#        print(box, end="\n"*2)
        
#    print(C_URL)
