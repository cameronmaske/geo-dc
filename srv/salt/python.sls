include:
  - requirements

# Download the Python 2.7.4 tarball.
python-2.7.4:
  file.managed:
    - name: /tmp/Python-2.7.4.tar.bz2
    - source: http://www.python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2
    - source_hash: sha1=deb8609d8e356b3388f33b6a4d6526911994e5b1
    - require:
      - pkg: requirements

# Extract it
extract-python:
  cmd:
    - cwd: /tmp
    - names:
      - tar -xvf Python-2.7.4.tar.bz2
    - run
    - require:
      - file: python-2.7.4

# Configure it
configure-python:
  cmd:
    - cwd: /tmp/Python-2.7.4
    - names:
      - apt-get build-dep python2.7 -y
      - ./configure
      - make
      - make install
    - run
    - require:
      - cmd: extract-python
