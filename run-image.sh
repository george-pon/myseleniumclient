#!/bin/bash
#
# test run image
#
function docker-run-myseleniumclient() {
    ${WINPTY_CMD} docker run -i -t --rm \
        -e http_proxy=${http_proxy} -e https_proxy=${https_proxy} -e no_proxy="${no_proxy}" \
        myseleniumclient:latest
}
docker-run-myseleniumclient
