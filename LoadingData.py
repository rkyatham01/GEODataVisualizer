import sqlite3
import json
import ssl
import urllib.request, urllib.parse, urllib.error

api_key = 42 #Sets the Api_key
serviceurl = "http://py4e-data.dr-chuck.net/json?"
#Can access this api ^ up there and this API works like Google API

connection = sqlite3.connect('dataoflocations.sqlite')
#Creates a SQL table connects to it

cursr = connection.cursor() #Creates a cursor you can start using .execute and create Tables in SQL

cursr.execute('''DROP TABLE IF EXISTS Locations
''')
#Creates the TABLE called Locations
cursr.execute('''
CREATE TABLE Locations (UniversityAddress TEXT, dataoflocations TEXT)''')

# To Ignore the SSL certificate errors
# You make a ctx object and verify the hostname to false and the mode to CERT_NONE
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

filehndlr = open("where.data") #creates a filehandler
count = 0
for line in filehndlr:
    UniversityAddress = line.rstrip() #strips the spacing to the right so nothing can mess with the format
    cursr.execute("SELECT dataoflocations FROM Locations WHERE UniversityAddress= ?",
        ((memoryview(UniversityAddress.encode())), )) 
        #Using memoryview uses a copy of the actual thing so
        #it creatly increases the efficiency of the code
        #Encodes the data of the UniversityAddress

    #The dictionary is created for creating the url
    #needs to have the "address : UniversityAddress and key : 42" for each line
    #which keeps adding to the url

    dictionaryCreated = dict()
    dictionaryCreated["address"] = UniversityAddress 
    #sets where the UniversityAddress is to what is inside address
    dictionaryCreated["key"] = api_key

    url = serviceurl + urllib.parse.urlencode(dictionaryCreated)
    #To use the api of the url, you have to parse both into one link
    #serviceurl + the encodedurl of dictionaryCreated
    #urlencode adds all the +s and question marks to the url at the end

    print("Retrieved", url, "link") #url is being retrieved here each iteration
    #Basically API is creating different urls for each university and giving the data
    #through requesting the url to be open like down here
    getsreadytogetParsed = urllib.request.urlopen(url, context=ctx)

    data = getsreadytogetParsed.read().decode() #Then it decodes it to Unicode
    #and put in data so this data can be read

    print("Retrieved", len(data), "number of characters in data")
    #data is the data that was requested and this prints # of characters in it
    count = count + 1

    parsedata = json.loads(data) #then you parse that json data
    #parsedata is the data that was requested in JSON form
    cursr.execute('''INSERT INTO Locations (UniversityAddress, dataoflocations)
            VALUES ( ?, ? )''', (memoryview(UniversityAddress.encode()), (data.encode()) ) )
    #have to encode because the tables in SQL read in UTF-8

    connection.commit() #commits to the sql
print("Done Loading the data")
