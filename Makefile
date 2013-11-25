prefix=/usr/local

all:

install:
	install -m 0755 generate_image.py $(prefix)/bin
