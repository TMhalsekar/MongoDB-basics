#
# Assignment5 Interface
# Name: 
#

from pymongo import MongoClient
import os
import sys
import json
from math import cos, sin, sqrt, atan2, radians

def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    if(cityToSearch=="" or cityToSearch==" "):

        with open(saveLocation1, "w") as output:
            output.write("")
        output.close()

    else:
        business_docs = collection.find({'city': {'$regex':cityToSearch, '$options':"$i"}})
        with open(saveLocation1, "w") as output:
            for business in business_docs:
                bname = business['name']
                baddress = business['full_address'].replace("\n", ", ")
                bcity = business['city']
                bstate = business['state']
                output.write(bname.upper() + "$" + baddress.upper() + "$" + bcity.upper() + "$" + bstate.upper() + "\n")
        output.close()

def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    business_docs = collection.find({'categories': {'$in': categoriesToSearch}},
                                    {'name': 1, 'latitude': 1, 'longitude': 1, 'categories': 1})
    lat_1 = float(myLocation[0])
    lon_1 = float(myLocation[1])
    R = 3959
    with open(saveLocation2, "w") as output:
        for business in business_docs:
            name = business['name']
            lat_2 = float(business['latitude'])
            lon_2 = float(business['longitude'])

            phi1 = radians(lat_1)
            phi2 = radians(lat_2)
            del_phi = radians(lat_2 - lat_1)
            del_lambda = radians(lon_2 - lon_1)
            a = (sin(del_phi / 2) * sin(del_phi / 2)) + (
                        cos(phi1) * cos(phi2) * sin(del_lambda / 2) * sin(del_lambda / 2))
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            d = R * c
            if d <= maxDistance:
                output.write(name.upper() + "\n")

    output.close()
