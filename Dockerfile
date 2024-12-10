FROM python:3.10

RUN apt-get update && apt-get install -y build-essential python3-dev libldap2-dev libsasl2-dev

RUN mkdir /opt/app

COPY ./requirements.txt /opt/app/requirements.txt
RUN pip3 install pip==24.3.1
RUN pip3 install -U -r /opt/app/requirements.txt

WORKDIR /opt/app/

COPY . /opt/app/

RUN chmod a+x scripts/wait-for-it.sh
RUN chmod a+x scripts/run.sh
