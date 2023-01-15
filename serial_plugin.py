# -*- coding: utf-8 -*-

import time
import serial
import serial.tools.list_ports

import pibooth
from pibooth.utils import LOGGER

__version__ = "0.0.1"

name = 'pibooth-core:serial'
SECTION = "Serial"

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    """Start serial connection"""
    LOGGER.info("serial startup")
    serial_ports = serial.tools.list_ports.comports()
    for port in serial_ports:
        LOGGER.info("Serial Port:" + str(port.device))
        if "USB" in str(port):
            arduino_serial_port = port.device
    
    LOGGER.info("selected serial port: "+ str(arduino_serial_port))
    app.serial = serial.Serial(port=str(arduino_serial_port),  baudrate=9600, timeout=2)
    try:
        LOGGER.info("serial connection successful")
        app._on_button_capture_held()
    except:
        LOGGER.info("Failed serial connection on port /dev/ttyUSB0")

@pibooth.hookimpl
def state_wait_do(app, events):
    if(app.serial == None):
        LOGGER.info("No serial connection. Initialize serial reconnect")
        serial_ports = serial.tools.list_ports.comports()
        for port in serial_ports:
            LOGGER.info("Serial Port:" + str(port.device))
            if "USB" in str(port):
                arduino_serial_port = port.device
        try:
            app.serial = serial.Serial(port=arduino_serial_port,  baudrate=9600, timeout=2)
            LOGGER.info("serial connection successful")
            app._on_button_capture_held()
        except:
            LOGGER.info("Failed serial connection on port /dev/ttyUSB0")

    lastline = app.serial.readline().decode('utf-8').strip()
    if lastline == "0":
        app._on_button_capture_held()