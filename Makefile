HUGO_PARAMS =
DEV_PARAMS = -D

all:

build:
	hugo ${HUGO_PARAMS} --minify

dev:
	hugo ${HUGO_PARAMS} ${DEV_PARAMS}

server:
	hugo server ${HUGO_PARAMS} ${DEV_PARAMS}

tarball: build
	tar czf page.tar.gz -C public .

.PHONY: tarball build
