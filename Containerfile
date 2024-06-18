# Options for if default build does not work on your machine
# Windows/Linux
# FROM python:3.12.1-bookworm
# Mac
# FROM amd64/python:3.12.1-bookworm
# Mac M1
# FROM arm64v8/python:latest
# Auto-select architecture
# FROM python:3.12

FROM python:3-slim-bookworm as common-base

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install dependencies

RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom
RUN apt-get clean && \
    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -f libldap-dev \
        libsasl2-dev \
        vim \
        default-libmysqlclient-dev \ 
        pkg-config \ 
        build-essential -y
RUN apt-get autoremove

FROM common-base as base-builder

# Upgrade pip and setuptools
RUN pip3 install -U pip setuptools

RUN mkdir -p /app/
WORKDIR /app/

# Stage 1: Extract dependency information from setup.py alone
# Allows caching until setup.py changes
FROM base-builder as dependencies

COPY setup.py .
COPY README.md .
RUN python setup.py egg_info

# Stage 2: Install dependencies based on information extracted from previous step

FROM base-builder as builder

# Configure 

RUN mkdir -p /install
COPY --from=dependencies /app/announcements.egg-info/requires.txt /tmp/
RUN sh -c 'pip install --no-warn-script-location --prefix=/install $(grep -e ^$ -m 1 -B 9999 /tmp/requires.txt) gunicorn'


# Everything up to here should be fully cacheable unless dependencies change

# Now we copy the application code

COPY . . 

# Stage 3: Install application
RUN sh -c 'pip install --no-warn-script-location --prefix=/install .'

# Stage 4: Install application into a temporary container to have both source and compiled files
# Compile static assets

FROM builder as static-builder

RUN cp -r /install/* /usr/local

# Stage 5: Install compiled static assets and support files into clean image

FROM common-base

RUN mkdir -p /app
COPY entrypoint.sh /app/
COPY --from=builder /install /usr/local
COPY --from=static-builder /app/static /app/static
COPY . /app

WORKDIR /app

RUN sh -c 'python manage.py collectstatic --no-input'
RUN mkdir -pv /var/log/gunicorn/
RUN mkdir -pv /var/run/gunicorn/
RUN mkdir -pv /var/www/announcements/static/
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

