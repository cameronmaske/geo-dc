import requests
import csv
from bs4 import BeautifulSoup

from models import Crime
from utils.models import get_or_make
from utils.logger import get_logger

logger = get_logger()


def translate_block(x, y, site_address):
    """
    Turns block coordinates into longitude and latitude
    """
    url = "http://citizenatlas.dc.gov/newwebservices/locationverifier.asmx/findLocation"
    params = {"str": site_address}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content)

    return {
        'lng': soup.findAll('longitude')[0].text,
        'lat': soup.findAll('latitude')[0].text
    }

def gather_crime_data():
    """
    This functions takes a CSV of Crime Incidents from 2013 from http://data.dc.gov/
    and stores it in a sqlite3 database (to be used to generate various other formats
    such as geojson later on).

    As we want geo data, we need the longitude and latitude of each Crime incident.
    Unfortunately, the data supplied by CSV is geolocated by three things...

    - BLOCKXCOORD (block x coordinates)
    - BLOCKYCOORD (block y coordinates)
    - BLOCKSITEADDRESS (block site address)

    It is currently not know how these map to longitude and latitude.
    The current method for determining is to use the block site address
    to query a dc.gov api endpoint named 'LocationVerifier' (http://citizenatlas.dc.gov/newwebservices/locationverifier.asmx)
    which returns the longitude and latitude.

    This is however very slow, with about 30k crime incident data points to be
    individually queried.

    Any improvements that meant the block coordinate system could be tranlated
    straight to longitude and latitude without having to hit this endpoint should
    be an incredible speed up.
    """
    csv_file = csv.DictReader(open('raw/crime.csv', 'rb'))

    for record in csv_file:
        try:
            # Get or create a database entry based on the CNC.
            crime, exists = get_or_make(Crime, cdn=record['CDN'])
            # Already in our database
            if exists and crime.latitude and crime.longitude:
                break

            coordinates = translate_block(
                record['BLOCKXCOORD'],
                record['BLOCKYCOORD'],
                record['BLOCKSITEADDRESS'])

            crime.longitude = coordinates['lng']
            crime.latitude = coordinates['lat']

            crime.block_y = record['BLOCKYCOORD']
            crime.block_x = record['BLOCKXCOORD']
            crime.block_address = record['BLOCKSITEADDRESS']

            crime.reported = record['REPORTDATETIME']
            crime.last_modified = record['LASTMODIFIEDDATE']

            crime.shift = record['SHIFT']
            crime.offense = record['OFFENSE']
            crime.method = record['METHOD']

            crime.ward = record.get('WARD')
            crime.anc = record.get('ANC')
            crime.district = record.get('DISTRICT')
            crime.psa = record.get('PSA')
            crime.neighborhood_cluster = record.get('NEIGHBORHOODCLUSTER')
            crime.business_improvement_district = record.get('BUSINESSIMPROVEMENTDISTRICT')

            crime.save()
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    gather_crime_data()
