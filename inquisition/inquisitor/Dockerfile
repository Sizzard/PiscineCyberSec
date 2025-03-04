FROM python:latest

RUN apt update -y && apt upgrade -y && apt install net-tools && apt-get install -y iputils-ping -y

RUN apt-get install libpcap-dev -y

COPY inquisitor.py script.sh /bin/

WORKDIR /bin/

RUN pip install scapy && pip install argparse

ENTRYPOINT ["/bin/bash", "/bin/script.sh"]