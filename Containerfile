#Windows/Linux
#FROM python:3.12.1-bookworm

#Mac
FROM amd64/python:3.12.1-bookworm

#Mac M1
#FROM arm64v8/python:latest

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom
RUN apt-get clean && \ 
    apt-get update -y && \
    apt-get upgrade -y && \ 
    apt-get install -f libldap-dev \
        libsasl2-dev \
        vim \
        build-essential -y
RUN apt-get autoremove
RUN apt-get install npm -y 

COPY . /app/

WORKDIR /app/

RUN pip install -r requirements.txt
RUN mv settings_local.templ.py settings_local.py
RUN python manage.py makemigrations  

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
