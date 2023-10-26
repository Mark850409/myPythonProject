FROM phpmyadmin/phpmyadmin
# APT Update/Upgrade, then install packages we need
RUN apt update && \
    apt upgrade -y && \
    apt autoremove && \
    apt install -y \
    vim

# Replace php.ini
COPY php.ini /usr/local/etc/php

# Remove old php.ini files
RUN rm /usr/local/etc/php/php.ini-development && \
    rm /usr/local/etc/php/php.ini-production

EXPOSE 8080 443