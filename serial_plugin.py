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
        app.serial = serial.Serial(port='/dev/ttyUSB0',  baudrate=9600, timeout=2)
        LOGGER.info("serial connection successful")
    except:
        LOGGER.info("Failed serial connection on port /dev/ttyUSB0")

@pibooth.hookimpl
def state_wait_do(app, events):
    if(app.serial == None):
        try:
            app.serial =  serial.Serial(port='/dev/ttyUSB0',  baudrate=9600, timeout=2)
        except:
            LOGGER.info("Failed serial connection on port /dev/ttyUSB0")
    else:
        lastline = app.serial.readline().decode('utf-8').strip()
        if lastline == "0":
            app._on_button_capture_held()