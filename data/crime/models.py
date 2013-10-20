from os import path
from peewee import *

# Get the current directory and filename (not used)
directory, filename = path.split(path.abspath(__file__))
# Change the output directory to dataset folders.
output_directory = directory.replace("data/crime", "datasets/crime")

database = SqliteDatabase(output_directory + '/crime.db')

class Crime(Model):
    """
    Based on http://data.dc.gov/Metadata.aspx?id=3
    """
    # Crime Complaint Number (CCN)
    cdn = CharField(unqiue=True)
    # Location coordinates.
    longitude = FloatField(null=True)
    latitude = FloatField(null=True)
    # The block x and y coords
    # These appear to be an internal longitude/latitude equivalents, but
    # it's unclear how they map to long/lat.
    block_y = FloatField()
    block_x = FloatField()
    block_address = CharField()
    # When was the crime reported
    reported = DateTimeField()
    # When as the data last modified
    last_modified = DateTimeField()
    # What shift did it occur on? E.g. Midnight
    shift = CharField()
    # What was the crime? E.g. Homicide
    offense = CharField()
    # What was it commited with? E.g. Knife
    method = CharField()

    # Ward
    ward = CharField(null=True)
    # Advisory Neighborhood Comission
    anc = CharField(null=True)
    # Ditrict
    district = CharField(null=True)
    # Police Service Area
    psa = CharField(null=True)
    neighborhood_cluster = CharField(null=True)
    # Business Improvement District
    business_improvement_district = CharField(null=True)


    class Meta:
        database = database

if __name__ == '__main__':
    database.connect()
    Crime.create_table()