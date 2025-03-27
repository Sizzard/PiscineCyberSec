FROM debian:latest

RUN apt update -y && apt upgrade -y && apt install net-tools && apt-get install -y iputils-ping -y

RUN apt install vsftpd -y

RUN useradd ftpuser && echo 'ftpuser:admin' | chpasswd && mkdir /home/ftpuser

RUN touch /home/ftpuser/test.txt

COPY vsftpd.conf /etc/

RUN chown -R ftpuser /home/ftpuser 

RUN service vsftpd restart

EXPOSE 21

CMD [ "/usr/sbin/vsftpd", "/etc/vsftpd.conf" ]