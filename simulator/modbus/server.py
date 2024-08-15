#!/usr/bin/env python3

import asyncio
import logging
import sys

from pymodbus import __version__ as pymodbus_version
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext
)
from pymodbus.server import (
    StartAsyncTcpServer
)

_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)

def setup_server():
    di_datablock = lambda : ModbusSequentialDataBlock(0x00, [0] * 4)
    co_datablock = lambda : ModbusSequentialDataBlock(0x10, [0] * 4)
    hr_datablock = lambda : ModbusSequentialDataBlock(0x20, [0] * 4)
    ir_datablock = lambda : ModbusSequentialDataBlock(0x30, [0] * 4)
    
    slave_context = ModbusSlaveContext(
        di = di_datablock(), 
        co = co_datablock(), 
        hr = hr_datablock(), 
        ir = ir_datablock()
    )
    
    slaves = {
        0x01: slave_context
    }
    
    server_context = ModbusServerContext(
        slaves = slaves, single = False)

    return server_context

async def run_async_server(server_context):
    address = ("0.0.0.0", 50502)
    server = await StartAsyncTcpServer(
        context=server_context,  # Data storage
        address=address  # listen address
    )
    
    return server


async def async_helper():
    server_context = setup_server()
    await run_async_server(server_context)


if __name__ == "__main__":
    asyncio.run(async_helper(), debug = True)
