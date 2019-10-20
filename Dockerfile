FROM python:3.7

MAINTAINER Thalia Technicie <www@thalia.nu>

# Try to keep static operation on top to maximise Docker cache utilisation

# Arguments
ARG install_dev_requirements=1

# Disable output buffering
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# Set up entrypoint and command
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["--help"]

# Create /eetfestijn dir
# Create log dir and log file
# Create app dir
RUN mkdir /eetfestijn && \
    mkdir -p /eetfestijn/log/ && \
    touch /eetfestijn/log/uwsgi.log && \
    chown -R www-data:www-data /eetfestijn && \
    mkdir -p /usr/src/app/

WORKDIR /usr/src/app/
COPY . /usr/src/app/

RUN cp /usr/src/app/resources/entrypoint.sh /usr/local/bin/entrypoint.sh && \
    cp /usr/src/app/resources/entrypoint_production.sh /usr/local/bin/entrypoint_production.sh && \
    rm -rf resources && \
    chmod +x /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint_production.sh

RUN pip install --no-cache-dir poetry && \
    poetry config settings.virtualenvs.create false

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    locales \
    gettext && \
    rm -rf /var/lib/apt

# Set the locale
RUN echo 'nl_NL.UTF-8 UTF-8' > /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN if [ "$install_dev_requirements" -eq 1 ]; then \
        poetry install --no-interaction; \
    else \
        echo "This will fail if the dependencies are out of date"; \
        poetry install --no-interaction --no-dev; \
    fi; \
    poetry cache:clear --all --no-interaction pypi
