#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""Options of the whole project"""
from os import path
import ConfigParser


OPTIONS = ConfigParser.ConfigParser()
OPTIONS.read(path.join(path.dirname(__file__), 'options.cfg'))
