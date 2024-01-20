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

WORKDIR /home/announcements
RUN git clone https://github.com/UCF/UCF-Announcements-Django

WORKDIR /home/announcements/UCF-Announcements-Django 
RUN git switch containerfile

WORKDIR /home/announcements/UCF-Announcements-Django
RUN pip install -r requirements.txt
RUN npm install
RUN cp settings_local.templ.py settings_local.py
RUN python manage.py deploy

CMD python manage.py runserver 0.0.0.0:8000