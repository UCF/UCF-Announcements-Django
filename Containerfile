FROM python:3.11-bookworm
ENTRYPOINT ["/bin/bash"]

WORKDIR /home

RUN apt-get clean && \ 
    apt-get update -y && \
    apt-get upgrade -y && \ 
    apt-get install -f libldap-dev \
        libsasl2-dev \
        build-essential \
        npm -y 
RUN pip install virtualenv
RUN virtualenv announcements 

WORKDIR /home/announcements
RUN git clone https://github.com/UCF/UCF-Announcements-Django

WORKDIR /home/announcements/UCF-Announcements-Django 
RUN git switch python3-upgrade

WORKDIR /home/announcements/bin
ENV VIRTUAL_ENV=../../announcements
RUN python3 -m virtualenv $VIRTUAL_ENV

WORKDIR /home/announcements/UCF-Announcements-Django
RUN pip install -r requirements.txt
RUN npm install
RUN python manage.py deploy

CMD python manage.py runserver 0.0.0.0:8004