#!/usr/bin/env python3

import asyncio
import logging
import sys
import json
import random
import time

import pymodbus.client as modbusClient
from pymodbus import ModbusException
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

glb_config = {}
runtime_args = {
    'temperature': 20,
    'cooling': False, 
    'heating': False, 
    'server_context': None
}

def setup_clients(): 
    clients = {}
    ac_client = modbusClient.AsyncModbusTcpClient(
        glb_config['ac-addr'],
        port=glb_config['ac-port']
    )
    clients['ac_client'] = ac_client
    
    thermostat_client = modbusClient.AsyncModbusTcpClient(
        glb_config['thermostat-addr'],
        port=glb_config['thermostat-port']
    )
    clients['thermostat_client'] = thermostat_client

    return clients

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


async def run_async_client(client, modbus_calls=None):
    await client.connect()
    assert client.connected
    if modbus_calls:
        await modbus_calls(client)
    client.close()

async def ac_calls(client):
    while True: 
        cooling = runtime_args['cooling']
        heating = runtime_args['heating']
        
        temperature = runtime_args['temperature']
        if temperature > 35: 
            cooling = True
        elif temperature < 25: 
            cooling = False 
        
        if temperature < 10: 
            heating = True
        elif temperature > 20:
            heating = False
            
        # update server args 
        runtime_args['server_context'].setValues(
            0x10, 
            0, 
            [cooling])
        runtime_args['server_context'].setValues(
            0x11, 
            0, 
            [heating])
                    
        try:     
            await client.write_coil(0x10, cooling, slave = 1)
            await client.write_coil(0x11, heating, slave = 1)
        except ModbusException:
            pass 
        
        time.sleep(1)
    
async def thermostat_calls(client): 
    # initialize thermostat temperature
    global runtime_args
    wr = await client.write_register(
        0x20, 
        runtime_args['temperature'], 
        slave = 1)
    
    while True: 
        try:    
            rr = await client.read_holding_registers(
                0x20, 
                1, 
                slave = 1)
            temperature = rr.registers[0]
            runtime_args['temperature'] = temperature 
            
            # update server args 
            print(runtime_args['server_context'].slaves())
            runtime_args['server_context'].get(1).setValues(
                0x20, 
                0, 
                [temperature])
            
            # natural heating 
            temperature += random.randint(-3, 3)
            # ac 
            if runtime_args['cooling']: 
                temperature -= 4
            if runtime_args['heating']:
                temperature += 4
            await client.write_register(
                0x20, 
                temperature, 
                slave = 1) 
        except ModbusException:
            pass 
        
        time.sleep(1)
         

async def run_async_server(server_context): 
    address = (
        glb_config['server-addr'], 
        glb_config['server-port'])
    server = await StartAsyncTcpServer(
        context = server_context,  # Data storage
        address = address  # listen address
    )
    return server

async def main(): 
    # read json config file
    global glb_config 
    with open('client-config.json') as f: 
        glb_config = json.load(f)
    
    global runtime_args    
    client_contexts = setup_clients()
    server_context = setup_server()
    runtime_args['server_context'] = server_context 
    
    await asyncio.gather(
        run_async_client(
            client_contexts['ac_client'], 
            modbus_calls = ac_calls), 
        run_async_client(
            client_contexts['thermostat_client'], 
            modbus_calls = thermostat_calls), 
        run_async_server(server_context)
    )

if __name__ == "__main__":
    asyncio.run(main(), debug = True)
