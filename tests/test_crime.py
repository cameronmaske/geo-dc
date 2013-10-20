from bs4 import BeautifulSoup

block_y = 138305
block_x = 397060

lat_cord = 38.91261123446170
long_cord = -77.03389715116880

with open('tests/crime.xml') as xml_file:
    respone = xml_file.read()
    soup = BeautifulSoup(respone)
    print soup
    print dir(soup.findAll('longitude').text
    print soup.findAll('latitude')[0].text
#data = doc['ReturnObject']['returnBlkAddrDataset']['xs:schema']['xs:element']['xs:complexType']['xs:choice']['xs:element']['xs:complexType']['xs:sequence']


#<CENTROIDX>396459</CENTROIDX>
#<CENTROIDY>138822</CENTROIDY>

#<LATITUDE>38.91726155448940</LATITUDE>
#<LONGITUDE>-77.04082371741050</LONGITUDE>


