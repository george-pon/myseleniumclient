#!/bin/bash
#
# test run image
#
function docker-run-myseleniumclient() {
    docker pull docker.io/georgesan/myseleniumclient:latest
    ${WINPTY_CMD} docker run -i -t --rm \
        -e http_proxy=${http_proxy} -e https_proxy=${https_proxy} -e no_proxy="${no_proxy}" \
        --cap-add SYS_ADMIN \
        docker.io/georgesan/myseleniumclient:latest
}
docker-run-myseleniumclient
