import requests
import shutil
from bs4 import BeautifulSoup

#returns dict in form {title:link}
def get_products():
    links_dict = {}
    url = "https://www.amazon.com/Best-Sellers/zgbs"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    products = soup.find_all("div", class_="zg_item zg_homeWidgetItem")
    for product in products:
        links = product.find_all("a",class_="a-link-normal")
        if(len(links) > 0):
            link = links[0].get("href")
            title = links[0].get_text()
            links_dict[title] = link
            
    return links_dict

def get_description(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    #feature bullets are the first description section, at the top of the page next to the product pictures
    feature_bullets = soup.find("div", id="feature-bullets")
    feature_bullet_string = ""
    if(feature_bullets is not None):
        text = feature_bullets.get_text()
        text = text.strip() 
        lines = text.split("\n")
        lines = lines[11:] #first 11 lines are a consistent javascript function
        for line in lines:
            line = line.strip()
            if(line == ''):
                continue
            else:
                feature_bullet_string += "- "+line+"\n"

    #now on to the lengthy description
    description = soup.find("div",id="productDescription")
    product_description = ""
    if(description is not None):
        product_description = description.get_text().strip()
        #print(product_description)

    full_description = feature_bullet_string+product_description
    return full_description

#bad right now because it only returns the first photo, but I don't really care because I just want to finish this fucking thing
def get_image(url, title):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    image_wrapper = soup.find(id="imgTagWrapperId")
    try:
        image = image_wrapper.find("img")
        image_url = image.get('src')

        invalid_characters = [" ","\\","/","$"]
        for char in invalid_characters:
            title.replace(char,"")
        filename = title+".jpg"
        r = requests.get(image_url, stream=True)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
        return filename
    except AttributeError:
        return -1

def get_price(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        price = soup.find("span",id="priceblock_ourprice").text
        price = price.replace("$","")
        price.strip()
        try:
            return float(price)
        except ValueError: #probably a price spread
            return -1 
    except AttributeError: #e.g. nonetype has no .text 
        return -1 

def get_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        title = soup.find("span",id="productTitle").text
        title = title.strip()
        return title
    except AttributeError:
        return -1


    

#something is broken because all of the titles are now invalid. I'll fix this tomorrow
def get_listables():
    base_url = "https://www.amazon.com"
    listables = []

    product_dict = get_products()

    for product in product_dict:
        temp_dict = {}
        url = base_url + product_dict[product]
        print(url)
        title = get_title(url)
        if(title == -1):
            print("invalid")
        else:
            temp_dict['title'] = title
            temp_dict['price'] = get_price(url)
            temp_dict['description'] = get_description(url)
            temp_dict['image'] = get_image(url, title) #filename of image
            listables.append(temp_dict)
    return listables

get_listables()    
