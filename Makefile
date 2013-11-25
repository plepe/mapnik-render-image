prefix=/usr/local

all:

install:
	install -m 0755 mapnik-render-image $(prefix)/bin
