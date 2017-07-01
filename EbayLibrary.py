from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
from difflib import SequenceMatcher

app_id = open("AppID.txt","r").read().strip() #strip gets rid of the newlines
dev_id = open("DevID.txt","r").read().strip()
cert_id = open("CertID.txt","r").read().strip()
auth_token = open("AuthnAuthToken.txt","r").read().strip()

#try:    
    #api = Trading(appid=app_id, devid=dev_id, certid=cert_id, token=auth_token,config_file=None)
#    api = Trading()
#    response = api.execute('GetUser', {})
#    print(response.dict())
#    print(response.reply) 
#    #response = api.execute('GetCategories',{})
#    #print(response.dict())

#except ConnectionError as e:
#    print(e)
#    print(e.response.dict())

def verifyAddItem(title,description,categoryID,price,pictures):
    api = Trading()
    myitem = {
        "Item":{
            "Title": title,
            "Description": description,
            "PrimaryCategory": {"CategoryID": categoryID},
            "StartPrice": price,
            "CategoryMappingAllowed": "true",
            "Country": "US",
            "ConditionID": "1000",
            "Currency": "USD",
            "DispatchTimeMax": "3",
            "ListingDuration": "Days_7",
            "ListingType": "Chinese",
            "PaymentMethods": "PayPal",
            "PayPalEmailAddress": "mcclane.howland@gmail.com",
            "PictureDetails": {"PictureURL": pictures},
            "PostalCode": "95125",
            "Quantity": "1",
            "ReturnPolicy": {
                "ReturnsAcceptedOption": "ReturnsNotAccepted",
                #"RefundOption": "MoneyBack",
                #"ReturnsWithinOption": "Days_30",
                #"Description": "If you are not satisfied, return the book for refund.",
                #"ShippingCostPaidByOption": "Buyer"
            },
            "ShippingDetails": {
                "ShippingType": "Flat",
                "ShippingServiceOptions": {
                    "ShippingServicePriority": "1",
                    "ShippingService": "UPS2ndDay",
                    "ShippingServiceCost": "0"
                }
            },
            "Site": "US"
        }
    }
    r = api.execute("VerifyAddItem", myitem)
    return r.reply


def get_category_id(keyword):
    try:
        api = Trading()

        callData = {
            'DetailLevel': 'ReturnAll',
            'CategorySiteID': 0,
            'LevelLimit': 4,
        }

        r = api.execute('GetCategories', callData)
        categories = r.dict()
        most_similar_category = {}
        max_similarity = -1
        for category in categories['CategoryArray']['Category']:
            similarity_ratio = SequenceMatcher(None,keyword,category['CategoryName']).ratio()
            if(similarity_ratio > max_similarity):
                most_similar_category = category
                max_similarity = similarity_ratio

        print("Most similar category: "+most_similar_category['CategoryName']+" at "+str(max_similarity)+" similarity")
        return most_similar_category['CategoryID'] 
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def upload_picture_from_filesystem(filepath):
    try:
        api = Trading()

        # pass in an open file
        # the Requests module will close the file
        files = {'file': ('EbayImage', open(filepath, 'rb'))}

        pictureData = {
            "WarningLevel": "High",
            "PictureName": "gtr2"
        }

        r = api.execute('UploadSiteHostedPictures', pictureData, files=files)
        response_dict = r.dict()
        #print(response_dict['SiteHostedPictureDetails'])
        #print(response_dict['SiteHostedPictureDetails']['FullURL'])
        image_url = response_dict['SiteHostedPictureDetails']['FullURL']
        return image_url



    except ConnectionError as e:
        print(e)
        print(e.response.dict())

