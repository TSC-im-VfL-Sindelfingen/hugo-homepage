HUGO_PARAMS =
DEV_PARAMS = -D
SERVER_PARAMS = --bind 0.0.0.0

all:

build:
	hugo ${HUGO_PARAMS} --minify

dev:
	hugo ${HUGO_PARAMS} ${DEV_PARAMS}

server:
	hugo server ${HUGO_PARAMS} ${SERVER_PARAMS}

dev-server:
	hugo server ${HUGO_PARAMS} ${SERVER_PARAMS} ${DEV_PARAMS}

tarball: build
	tar czf page.tar.gz -C public .

.PHONY: tarball build

trigger-sync-to-stage:
	ssh tsc-homepage@hh.wolf-stuttgart.net

sync-to-stage-manual:
	rsync -ahPv --delete --delete-delay --info=progress2 --chown tsc-homepage:tsc-homepage public/ root@hh.wolf-stuttgart.net:/srv/http/tsc/hugo/
