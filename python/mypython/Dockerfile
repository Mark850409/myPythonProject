FROM php:7.4-apache
WORKDIR /var/www/html
COPY requirements.txt ./
RUN apt-get -y update \
&& apt-get install -y python3 python3-pip \
&& apt install vim -y \
&& a2enmod rewrite \
&& a2enmod ssl \
&& a2enmod headers \
&& a2enmod proxy \
&& a2enmod proxy_http \
&& a2enmod proxy_balancer \
&& a2enmod cgi \
&& apt-get install -y --no-install-recommends \
&& python3 -m pip install --upgrade pip \ 
&& pip install --no-cache-dir -r requirements.txt \
&& mkdir -p /var/www/html/templates
COPY letsencrypt /etc/letsencrypt/
COPY apache/apache2.conf /etc/apache2/
COPY apache/000-default.conf /etc/apache2/sites-available/
COPY apache/ports.conf /etc/apache2/
COPY main.py /var/www/html
COPY my_config.ini /var/www/html
COPY index.html /var/www/html/templates
COPY DigiCertGlobalRootCA.crt.pem /var/www/html
RUN chmod +X main.py && chmod 755 main.py 
EXPOSE 80 22