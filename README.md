# myseleniumclient

seleniumclient image by debian 11 python 3 for https://github.com/SeleniumHQ/docker-selenium



### tag

* monthly202205, debian11, stable, latest
    * first release

### how to use

outputs JSON data.

```
    # when running on Windows , set below
    WINPTY_CMD=winpty.exe

    # run image
    docker pull docker.io/georgesan/myseleniumclient:latest
    ${WINPTY_CMD} docker run -i -t --rm \
        -e http_proxy=${http_proxy} -e https_proxy=${https_proxy} -e no_proxy="${no_proxy}" \
        --cap-add SYS_ADMIN \
        docker.io/georgesan/myseleniumclient:latest \
        access-url-and-screen-shot.py --screenshot https://www.google.com/
```

outputs below.

```
{
  "title": "Google",
  "screenshot": "iVBORw0KGgoAAAANSrk..."
}
```

screenshot is PNG file data encoded base64.

