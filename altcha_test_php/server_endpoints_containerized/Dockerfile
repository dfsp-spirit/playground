# Dockerfile to run the Altcha endpoints in a Slim app on the FrankenPHP server.
#
# To build and run the Docker image from this Docker file, do:
#
#    docker build -t altchaendpoints .
#    docker run -it -p 80:80 -p 443:443 --rm --name my-altchaendpoints altchaendpoints
#

FROM dunglas/frankenphp
RUN apt-get update && \
    apt-get install -y libnss3-tools && \
    apt-get clean && \
	rm -rf /var/lib/apt/lists/*
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

ENV SERVER_NAME=altcha.webapps.nfdi4earth.de
# If you want to disable HTTPS, use this value instead:
#ENV SERVER_NAME=:80

# Enable PHP production settings
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Replace with a secret. Do not put the real one into your version control system.
ENV ALTCHA_SERVER_KEY=bananeinderbirne


COPY . /app/

ARG USER=www-data

RUN \
	# Use "adduser -D ${USER}" for alpine based distros
	useradd -D ${USER}; \
	# Add additional capability to bind to port 80 and 443
	setcap CAP_NET_BIND_SERVICE=+eip /usr/local/bin/frankenphp; \
	# Give write access to /data/caddy and /config/caddy
	chown -R ${USER}:${USER} /data/caddy && chown -R ${USER}:${USER} /config/caddy

RUN chmod -R 775  /app/vendor/ && \
    chown -R $USER:$USER /app/vendor/

USER ${USER}


RUN composer install