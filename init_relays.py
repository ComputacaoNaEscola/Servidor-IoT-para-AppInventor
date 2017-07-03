#!/usr/bin/env python
# encoding: utf-8

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(12, 1)
GPIO.output(16, 1)
GPIO.output(20, 1)
GPIO.output(21, 1)
