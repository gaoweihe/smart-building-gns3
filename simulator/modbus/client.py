#!/usr/bin/env python3
"""Pymodbus asynchronous client example.

usage::

    client_async.py [-h] [-c {tcp,udp,serial,tls}]
                    [-f {ascii,rtu,socket,tls}]
                    [-l {critical,error,warning,info,debug}] [-p PORT]
                    [--baudrate BAUDRATE] [--host HOST]

    -h, --help
        show this help message and exit
    -c, -comm {tcp,udp,serial,tls}
        set communication, default is tcp
    -f, --framer {ascii,rtu,socket,tls}
        set framer, default depends on --comm
    -l, --log {critical,error,warning,info,debug}
        set log level, default is info
    -p, --port PORT
        set port
    --baudrate BAUDRATE
        set serial device baud rate
    --host HOST
        set host, default is 127.0.0.1

The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import asyncio
import logging
import sys

import pymodbus.client as modbusClient
from pymodbus import ModbusException


_logger = logging.getLogger(__file__)
_logger.setLevel("DEBUG")

def setup_async_client():
    client = modbusClient.AsyncModbusTcpClient(
        "127.0.0.1",
        port=50502
    )

    return client


async def run_async_client(client, modbus_calls=None):
    await client.connect()
    assert client.connected
    if modbus_calls:
        await modbus_calls(client)
    client.close()


async def run_a_few_calls(client):
    try:
        rr = await client.read_holding_registers(0x00, 2, slave=1)
        assert rr.registers[0] == 18
        assert rr.registers[1] == 18
    except ModbusException:
        pass


async def main(cmdline=None):
    testclient = setup_async_client()
    await run_async_client(testclient, modbus_calls=run_a_few_calls)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
