FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3-pip
RUN pip install modbus-tcp-simulator
