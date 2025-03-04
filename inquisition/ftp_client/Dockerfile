FROM debian:latest

RUN apt update -y && apt upgrade -y && apt install net-tools && apt-get install -y iputils-ping -y

RUN apt install ftp -y

ENTRYPOINT ["tail", "-f", "/dev/null"]