FROM nginx

RUN apt-get update
RUN apt-get install -y wget

COPY nginx.conf /etc/nginx/ 
COPY index.html /data/www/
COPY test.html /data/www/


