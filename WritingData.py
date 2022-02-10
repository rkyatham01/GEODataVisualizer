import json
import sqlite3

connection = sqlite3.connect('dataoflocations.sqlite') #connects to the database
cursr = connection.cursor() #Creates a cursor

cursr.execute('SELECT * FROM Locations')
#Selects everything from the Locations Table

file = "where.js" #defines a file 
fhand = open(file, 'w', encoding="utf-8")
#opens the file in write mode

fhand.write("Data = [\n") #Writes it in a specific format where it goes to the next line for each [

count = 0 #Counter for the if statement

for row in cursr :
    data = str(row[1].decode()) #Data has all the data of the object

    jsonFile = json.loads(str(data)) #converts it into string and loads it into JSON format of array of strings
    
    latitude = jsonFile["results"][0]["geometry"]["location"]["lat"] #finds the latitude of university
    longitude = jsonFile["results"][0]["geometry"]["location"]["lng"] #find the longitude of university

    where = jsonFile['results'][0]['formatted_address'] #gets the formatted address
    where = where.replace("'", "") #fixes the format of it

    count = count + 1
    if count > 1 : 
        fhand.write(",\n") #every time after the first file has been inputted it makes a , at the end
        # and then proceeds to go to the next line

    print(where, "is the address and the lattitude is",latitude,"and the longitude is",longitude)
    #prints the address with the lat and long seperate

    OutputtoWriteTo = "["+str(latitude)+","+str(longitude)+", '"+where+"']"
    #OutputtoWriteTo is the format of how the information that has been grabbed from the jsonFile is 
    #written in the where.js file

    fhand.write(OutputtoWriteTo) #writes it here

fhand.write("\n];\n") #writes to end the format of writing to the js file
cursr.close() #closes the cursor
fhand.close() #closes the file handler
print("Done Writing the data")
