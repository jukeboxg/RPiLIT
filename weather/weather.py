import urllib2
import json, requests
import csv
import math
import sys
import xml.etree.ElementTree as ET

class Weather:
    key = "d747fd0d14972dfb091760ee130916de"
    lat=0.0
    lon=0.0
    ipURL="https://ip.seeip.org/json"
    ip = "0.0.0.0"
    cityCode = "s0000769"
    province= "QC"
    city = ""
    myLat = ""
    myLong = ""
    shortestDistance = 0.0
    wUrl = "y"

    def __init__(self):
	pass
        #self.fetchIp()
        #self.fetchLocation()
        #self.fetchCityCode()
        
	#self.writeToFile()
        
    def reInitialize(self):
        self.getWeatherDataURL()
        self.getWeatherInformation()

    def fetchIp(self):
        url = requests.get(self.ipURL)
        ipText = json.loads(url.text)
        self.ip = ipText['ip']
        #print(self.ip)        
	
    def fetchLocation(self):
        locURL = "http://api.ipstack.com/" + self.ip + "?access_key=" + self.key
        url = requests.get(locURL)
	locText = json.loads(url.text)
        self.lat = locText['latitude']
        self.lon = locText['longitude']
        #print(str(self.lat) + "," + str(self.lon))

    def fetchCityCode(self):
        url = "http://dd.weather.gc.ca/citypage_weather/docs/site_list_provinces_en.csv"
        cityPage = urllib2.urlopen(url)

        fieldnames = ['Codes', 'English Names', 'Province Codes', 'Latitude', 'Longitude']
        city = "N/A"
        cr =csv.DictReader(cityPage, fieldnames = fieldnames)
        self.shortestDistance = 100000.00

        for row in cr:
            if row['Province Codes'] != "HEF": 
	        try:
	            #print(row['English Names'])
	            latitude = float(row['Latitude'][:-1])
	            longitude = float(row['Longitude'][:-1])
                    if row['Latitude'][-1:] == "S":
                        latitude = latitude * -1
                    if row['Longitude'][-1:] == "W":
                        longitude = longitude * -1
                    #print(str(latitude) + "," + str(longitude))
	            difference = self.coordinateDifference(latitude,longitude,self.lat,self.lon)
                    #print (difference)
	            if difference < self.shortestDistance:
	                self.shortestDistance = difference
	                self.city =row['English Names']
                        self.cityCode = row['Codes']
                        self.province = row['Province Codes']
                        #print(self.city + "," + str(self.shortestDistance))
	        except Exception as e:
		    print(e)
                    #sys.exit()
                    #pass
        #print(city)
        #print(self.cityCode)

    def coordinateDifference(self,latitude,longitude,myLatitude,myLongitude):
        return math.sqrt(math.pow(latitude-myLatitude,2)+math.pow(longitude-myLongitude,2))

    def getWeatherDataURL(self):
        self.wUrl ="http://dd.weather.gc.ca/citypage_weather/xml/"+self.province+"/"+self.cityCode+"_e.xml"
        print(self.wUrl)


    def getWeatherInformation(self):
        data = urllib2.urlopen(self.wUrl)
        tree = ET.parse(data)
        root = tree.getroot()
        print(tree.find('currentConditions').find('temperature').text)
        print(tree.find('currentConditions').find('humidex').text)         

    def writeToFile(self):
        f = open("/home/pi/RPiLIT/weather/weatherInformation.txt","w")
        f.write(self.cityCode + ";" + self.city + ";" + self.province + ";" + str(self.lat) + ";" + str(self.lon) + ";" + self.wUrl)
        f.close()


w1 = Weather()
w1.reInitialize()
print("Completed sucessfully")
