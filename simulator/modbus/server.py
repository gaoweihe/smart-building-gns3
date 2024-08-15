#!/usr/bin/env python3

import asyncio
import logging
import sys

from pymodbus import __version__ as pymodbus_version
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import (
    StartAsyncSerialServer,
    StartAsyncTcpServer,
    StartAsyncTlsServer,
    StartAsyncUdpServer,
)

_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)

def setup_server():
    datablock = lambda : ModbusSequentialDataBlock(0x00, [18] * 4)
    
    slave_context = ModbusSlaveContext(
        di=datablock(), co=datablock(), hr=datablock(), ir=datablock()
    )
    single = True
    
    server_context = ModbusServerContext(slaves=slave_context, single=single)

    return server_context

async def run_async_server(server_context):
    address = ("0.0.0.0", 50502)
    server = await StartAsyncTcpServer(
        context=server_context,  # Data storage
        address=address  # listen address
    )
    
    return server


async def async_helper():
    """Combine setup and run."""
    _logger.info("Starting...")
    server_context = setup_server()
    await run_async_server(server_context)


if __name__ == "__main__":
    asyncio.run(async_helper(), debug=True)
