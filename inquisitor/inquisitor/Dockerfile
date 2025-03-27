FROM python:latest

RUN apt update -y && apt upgrade -y && apt install net-tools && apt-get install -y iputils-ping -y

RUN apt-get install libpcap-dev -y

COPY inquisitor.py script.sh /bin/

WORKDIR /bin/

RUN pip install scapy && pip install argparse

ENTRYPOINT [ "python", "inquisitor.py", "10.10.8.2", "02:42:0a:0a:08:02", "10.10.8.4", "02:42:0a:0a:08:04"]

# ENTRYPOINT ["/bin/bash", "/bin/script.sh"]