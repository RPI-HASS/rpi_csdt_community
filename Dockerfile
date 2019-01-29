FROM ubuntu
MAINTAINER Chinedu Amadi-Ndukwe <chinedua@umich.edu>

RUN apt-get update && apt-get install -y python python-pip wget

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get install -y sudo
RUN apt-get install -y apt-utils
RUN apt-get install -y gnupg2
RUN apt-get install -y curl
RUN apt-get install -y nodejs
RUN apt-get install -y npm

COPY . /csdt_site
WORKDIR /csdt_site
RUN chmod +x setup.sh && ./setup.sh


RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install Django
RUN pip install psycopg2-binary

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
