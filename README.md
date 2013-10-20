Geo data for D.C
================

A collection of geospatial data for Washington D.C.


Datasets (and demos!)
---------------------

* [Crime incidents from 2013](https://github.com/cameronmaske/geo-dc/blob/master/datasets/crime/crime.geojson) - Taken from [http://data.dc.gov/](http://data.dc.gov/)
* [Neighborhoods](https://github.com/cameronmaske/geo-dc/blob/master/datasets/neighborhoods/neighorhoods.geojson) - Credit to [@justgrimes](https://twitter.com/justgrimes) and [The Washington Post](http://apps.washingtonpost.com/investigative/homicides/)
* [Airbnb listings](https://github.com/cameronmaske/geo-dc/blob/master/datasets/airbnb/airbnb.geojson)

Project structure
-----------------
The project is split into two parts

'/data' - Holds the python code to generate, gather and sanitize the data.

'/datasets'/ - Holds the sanitized data.
This can be in several formats

    1. [GeoJSON](http://geojson.org/). [Supported by GitHub](https://github.com/blog/1528-there-s-a-map-for-that)!.
    2. Good old fashioned CSV.
    3. A sqlite3 database.


Installation
------------
The projects uses Vagrant (1.2.7) to provision an Ubuntu 12.04 VM where all the code is run. It should run on other enviroments, but Vagrant let's you recreate an agnostic development enviroment. To install vagrant.

1. [Download and install Vagrant 1.2.7](http://downloads.vagrantup.com/tags/v1.2.7)
2. [Download and install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
3. [Install Salty Vagrant](https://github.com/saltstack/salty-vagrant)

    vagrant plugin install vagrant-salt

4. Start up vagrant (This may take several minutes). In this directory run

    vagrant up

5. SSH into the vagrant machine.

    vagrant ssh


Contributing
------------

Contributes are welcome! For new datasets, the minimum requirement is a GeoJSON file.


Todos
------------

1. Tests!
2. Document approach to datasets.
3. More datasets. Add any suggestions in an Issue.


Author
----------
[Cameron Maske](http://www.cameronmaske.com). Feel free to [drop me a tweet](http://www.twitter.com/cameronmaske) with your thoughts!

