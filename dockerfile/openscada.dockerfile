FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
EXPOSE 10002
RUN apt update && apt install -y wget 
RUN echo "deb http://ftp.oscada.org/OpenSCADA/LTS/Ubuntu/22.04 ./" | tee -a /etc/apt/sources.list
RUN wget -P /etc/apt/trusted.gpg.d http://ftp.oscada.org/Misc/openscada-archive-keyring.asc
RUN apt-get update 
RUN apt-get install -y openscada-model-aglks 
RUN apt-get install -y openscada-server 
RUN systemctl enable openscada-server
ENV DEBIAN_FRONTEND=dialog
ENTRYPOINT service openscada-server start && tail -f /dev/null
