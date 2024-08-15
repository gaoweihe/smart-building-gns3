#!/usr/bin/env python3

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
