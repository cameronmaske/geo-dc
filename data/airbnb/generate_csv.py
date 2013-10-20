from os import path
from csv import DictWriter
from models import AirbnbListing

def create_csv(filename="airbnb.csv"):
    """
    Generates a CSV based all stored AirBnb listings
    """
    # Query for all listings.
    airbnb_listings = AirbnbListing.select()
    # Get the current directory and filename (not used)
    directory, filename = path.split(path.abspath(__file__))
    # Change the output directory to dataset folders.
    output_directory = directory.replace("data/airbnb", "dataset/airbnb")
    f = open("{}/{}".format(output_directory, filename), 'wb')

    # Get all possible field names from keys.
    keys = airbnb_listings[0].as_dict().keys()
    csv_file = DictWriter(f, keys)
    csv_file.writeheader()
    for airbnb in airbnb_listings:
        csv_file.writerow(airbnb.as_dict())


if __name__ == '__main__':
    create_csv()
