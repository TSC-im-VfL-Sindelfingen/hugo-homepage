HUGO_PARAMS =
DEV_PARAMS = -D

all:

build:
	hugo ${HUGO_PARAMS} --minify

dev:
	hugo ${HUGO_PARAMS} ${DEV_PARAMS}

server:
	hugo server ${HUGO_PARAMS}

dev-server:
	hugo server ${HUGO_PARAMS} ${DEV_PARAMS}

tarball: build
	tar czf page.tar.gz -C public .

.PHONY: tarball build


sync-to-stage:
	rsync -ahPv --delete --delete-delay --info=progress2 public/ christian@hh.wolf-stuttgart.net:/srv/http/tsc/hugo/
