FROM debian:latest

USER root

RUN apt-get update -y && apt-get upgrade -y && apt-get install curl -y
RUN apt-get install tor -y
RUN apt-get install nginx -y

COPY nginx/index.html  /var/www/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]