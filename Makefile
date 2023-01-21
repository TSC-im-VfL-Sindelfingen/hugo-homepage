HUGO_PARAMS = -D

all:

build:
	hugo ${HUGO_PARAMS}

tarball: build
	tar czf page.tar.gz -C public .

.PHONY: tarball build
