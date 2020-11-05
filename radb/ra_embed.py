# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 11:48:27 2020

@author: fischpet
"""

import os
import configparser

from radb.db import DB
from radb.typesys import ValTypeChecker
from radb.views import ViewCollection
from radb.ast import Context

def ra_init(config_path, dbname):
    # read system defaults:
    sys_configfile = os.path.join(config_path, 'sys.ini')
    sys_config = configparser.ConfigParser()
    sys_config.read(sys_configfile)
    defaults = dict(sys_config.items(configparser.DEFAULTSECT))
    config = configparser.ConfigParser(defaults)

    configured = dict(config.items(configparser.DEFAULTSECT))

    configured['db.database'] = dbname

    db = DB(configured)

    # initialize type system:
    check = ValTypeChecker(configured['default_functions'], configured.get('functions', None))

    context = Context(configured, db, check, ViewCollection())
    return context, db.share_connection()