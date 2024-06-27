# Dockerfile to run the Altcha endpoints in a Slim app on the FrankenPHP server.
#
# To build and run the Docker image from this Docker file, do:
#
#    docker build -t altchaendpoints .
#    docker run -it --rm --name my-altchaendpoints altchaendpoints
#

FROM dunglas/frankenphp
RUN apt-get update && \
    apt-get clean && \
	rm -rf /var/lib/apt/lists/*
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN composer install
COPY . /app/public