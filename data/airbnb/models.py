from os import path
from peewee import *

# Get the current directory and filename (not used)
directory, filename = path.split(path.abspath(__file__))
# Change the output directory to dataset folders.
output_directory = directory.replace("data/crime", "dataset/crime")

database = SqliteDatabase(output_directory + '/airbnb.db')


class AirbnbListing(BaseModel):
    airbnb_id = CharField(unqiue=True)
    room_type = CharField(null=True)
    bed_type = CharField(null=True)
    neighbourhood = CharField()
    description = TextField()
    longitude = FloatField()
    latitude = FloatField()
    bedrooms = IntegerField()
    accommodates = IntegerField()
    bathrooms = FloatField(null=True)
    price = IntegerField()

    class Meta:
        database = database

    def as_dict(self):
        try:
            price_per_bedroom = float(self.price) / self.bedrooms
        except:
            price_per_bedroom = None

        try:
            price_per_accommodates = float(self.price) / self.accommodates
        except:
            price_per_accommodates = None

        return {
            'url': 'https://www.airbnb.co.uk/rooms/{}'.format(self.airbnb_id),
            'room_type': self.room_type,
            'bed_type': self.bed_type,
            'description': self.description.encode('utf-8'),
            'longitude': self.longitude,
            'latitude': self.latitude,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'neighbourhood': self.neighbourhood,
            'accommodates': self.accommodates,
            'price': self.price,
            'price per bedroom': price_per_bedroom,
            'price per accommodates': price_per_accommodates
        }

if __name__ == '__main__':
    database.connect()
    AirbnbListing.create_table()