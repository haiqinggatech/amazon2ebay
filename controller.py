import requests
import AmazonScraper
import EbayLibrary

print("getting products from amazon")
listables = AmazonScraper.get_listables()
print(str(len(listables))+" items retrieved from amazon")
for item in listables:
    categoryID = EbayLibrary.get_category_id(item['category']) #returns most similar category id








