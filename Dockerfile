FROM debian:bullseye

ENV MYSELENIUMCLIENT_VERSION build-target
ENV MYSELENIUMCLIENT_VERSION debian11
ENV MYSELENIUMCLIENT_VERSION latest
ENV MYSELENIUMCLIENT_VERSION stable
ENV MYSELENIUMCLIENT_IMAGE docker.io/georgesan/myseleniumclient

ENV DEBIAN_FRONTEND noninteractive

# set locale
RUN apt-get update && \
    apt-get install -y locales  apt-transport-https  ca-certificates  software-properties-common && \
    localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8 && \
    apt-get clean
ENV LANG ja_JP.utf8

# set timezone
# humm. failed at GitLab CI.
# RUN rm -f /etc/localtime ; ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN rm /etc/localtime ; echo Asia/Tokyo > /etc/timezone ; dpkg-reconfigure -f noninteractive tzdata
ENV TZ Asia/Tokyo

# install man pages
RUN apt-get install -y man-db  manpages && apt-get clean

# install etc utils
RUN apt-get install -y \
        bash-completion \
        curl \
        dnsutils \
        emacs-nox \
        expect \
        gettext \
        git \
        gnupg2 \
        iproute2 \
        jq \
        lsof \
        make \
        netcat \
        net-tools \
        procps \
        python3 \
        python3-pip \
        rsync \
        sudo \
        tcpdump \
        traceroute \
        tree \
        unzip \
        vim \
        w3m \
        wget \
        zip \
        chromium-driver \
        fonts-ipafont fonts-noto-cjk \
    && apt-get clean all

# install python selenium library
RUN pip3 install selenium

# add docker entry point shell
ADD docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ADD bin /usr/local/bin
RUN chmod +x /usr/local/bin/*.sh

# add sudo user
# https://qiita.com/iganari/items/1d590e358a029a1776d6 Dockerコンテナ内にsudoユーザを追加する - Qiita
# ユーザー名 debian
# パスワード hogehoge
RUN groupadd -g 1000 debian && \
    useradd  -g      debian -G sudo -m -s /bin/bash debian && \
    echo 'debian:hogehoge' | chpasswd && \
    echo 'Defaults visiblepw'            >> /etc/sudoers && \
    echo 'debian ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# use normal user debian
USER debian

ENV HOME /home/debian
ADD inputrc      $HOME/.inputrc
ADD bashrc       $HOME/.bashrc
ADD bash_profile $HOME/.bash_profile
ADD vimrc        $HOME/.vimrc
ADD emacsrc      $HOME/.emacs
ENV ENV          $HOME/.bashrc
WORKDIR          $HOME

CMD ["/usr/local/bin/docker-entrypoint.sh"]

