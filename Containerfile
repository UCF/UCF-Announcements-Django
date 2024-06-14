# Windows/Linux
# FROM python:3.12.1-bookworm

# Mac
# FROM amd64/python:3.12.1-bookworm

# Mac M1
# FROM arm64v8/python:latest

FROM python:3.12


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
	nginx \
	systemctl \
        build-essential -y
RUN apt-get autoremove

RUN mkdir -pv /var/log/gunicorn/
RUN mkdir -pv /var/run/gunicorn/
RUN mkdir -pv /var/www/announcements/static/

COPY . /app/

WORKDIR /app/

RUN pip install -r requirements.txt
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py migrate

COPY /config/nginx/announcements.conf /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/announcements.conf /etc/nginx/sites-enabled/announcements.conf

RUN systemctl enable nginx

EXPOSE 80

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:80 wsgi:application"]
