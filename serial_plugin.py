# -*- coding: utf-8 -*-

import time
import serial

import pibooth
from pibooth.utils import LOGGER

__version__ = "0.0.1"

name = 'pibooth-core:serial'
SECTION = "Serial"

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    """Start serial connection"""
    LOGGER.info("serial startup")
    try:
        serial_ports = serial.tools.list_ports.comports()
        LOGGER.info("Serial Port:" + serial_ports)
        app.serial = serial.Serial(port=serial_ports[0],  baudrate=9600, timeout=2)
        LOGGER.info("serial connection successful")
        app._on_button_capture_held()
    except:
        LOGGER.info("Failed serial connection on port /dev/ttyUSB0")

@pibooth.hookimpl
def state_wait_do(app, events):
    if(app.serial.isOpen()):
        try:
            serial_ports = serial.tools.list_ports.comports()
            app.serial = serial.Serial(port=serial_ports[0],  baudrate=9600, timeout=2)
        except:
            LOGGER.info("Failed serial connection on port /dev/ttyUSB0")
    else:
        lastline = app.serial.readline().decode('utf-8').strip()
        if lastline == "0":
            app._on_button_capture_held()