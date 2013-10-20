include:
    - requirements
    - python

# Create the Python Virtual enviroment.
/virtual-env:
    virtualenv.managed:
        - no_site_packages: True
        - requirements: /vagrant/requirements.txt
        - python: python2.7
        - require:
            - pkg: requirements
            - cmd: configure-python

# Make it so we automatically activate the virtualenv.
/home/vagrant/.bashrc:
    file.append:
        - text:
            - source /virtual-env/bin/activate
            - cd /vagrant/