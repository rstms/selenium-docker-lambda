FROM python:3.9.1-slim-buster

ARG USER

ENV USER=$USER
ARG UID
ENV UID=$UID
ARG GID
ENV GID=$GID

WORKDIR /root

# upgrade apt and install debian packages
RUN apt-get -y update \
  && apt-get -y install \
    bsdmainutils \
    curl \
    default-mysql-client \
    inetutils-ping \
    jq \
    less \
    locales \
    make \
    net-tools \
    openssh-client \
    procps \
    socat \
    sudo \
    vim \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# upgrade pip 
RUN python -m pip install --upgrade pip \
  && pip install --upgrade setuptools

COPY scripts/ /usr/local/bin

# pre-install python modules
WORKDIR /root
COPY home/src/setup.cfg .
RUN pip install $(setup-modules <setup.cfg)

# create and configure user accounts and groups
RUN \
  addgroup -gid 1201 selenium && \
  adduser -uid 1200 -gid 1201 --disabled-password --gecos '' selenium && \
  addgroup -gid $UID $USER && \
  adduser -uid $UID -gid $UID --disabled-password --gecos '' $USER && \
  adduser $USER selenium && \
  adduser $USER sudo && \
  echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


# copy module source to home directory
WORKDIR /home/$USER
COPY home/ .
RUN chown -R $USER.$USER .

WORKDIR /home/$USER/src
RUN sudo pip install -e .
RUN sudo pip install -e .[test]

WORKDIR /home/$USER
USER $USER

ENTRYPOINT [ "entrypoint.sh" ]
CMD [ "run" ]
