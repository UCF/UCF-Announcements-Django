#Windows/Linux
#FROM python:3.12.1-bookworm

#Mac
#FROM amd64/python:3.12.1-bookworm

#Mac M1
FROM arm64v8/python:latest

WORKDIR /home

RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom
RUN apt-get clean && \ 
    apt-get update -y && \
    apt-get upgrade -y && \ 
    apt-get install -f libldap-dev \
        libsasl2-dev \
        build-essential -y
RUN apt-get autoremove
RUN apt-get install npm -y 

WORKDIR /home/announcements
RUN git clone https://github.com/UCF/UCF-Announcements-Django

WORKDIR /home/announcements/UCF-Announcements-Django 
RUN git switch containerfile

WORKDIR /home/announcements/UCF-Announcements-Django
RUN pip install -r requirements.txt
RUN npm install
COPY settings_local.dev.py settings_local.py
RUN python manage.py migrate
RUN python manage.py loaddata audience

EXPOSE 8004
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8004"]