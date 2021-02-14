FROM python:3.9.1-slim-buster

ARG PROJECT
ENV PROJECT=$PROJECT
ENV USER=$PROJECT
ARG UID
ENV UID=$UID
ARG GID
ENV GID=$GID

WORKDIR /root

# upgrade apt and install debian packages
COPY apt-packages .
RUN apt-get -y update && \
  apt-get -y install $(echo $(cat /root/apt-packages)) && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# upgrade pip and install python modules
COPY src/$PROJECT/requirements*.txt ./
RUN python -m pip install --upgrade pip && \
  pip install -r requirements.txt && \
  pip install -r requirements-test.txt

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
COPY src/$PROJECT ./src/
RUN chown -R $USER.$USER src

WORKDIR /home/$PROJECT/src
RUN pip install .

USER $USER
WORKDIR /home/$USER

CMD $PROJECT --server
