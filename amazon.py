import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.com/Best-Sellers/zgbs"
r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
products = soup.find_all("div", class_="zg_item zg_homeWidgetItem")
links = products[0].find_all("a", class_="a-link-normal")
#links I don't want: product reviews and stars and image.
if(len(links) > 0):
    print(links[0].get_text())

