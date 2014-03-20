#!/usr/bin/python

from sys import argv
import ConfigParser, os
import redis
import datetime
import hashlib

class MaxOutConfig():
    def __init__(self):
        self.read_config()
    
    def read_config(self): 
        try:
            config_file = argv[1]
        except IndexError:
            config_file = 'setup.cfg'

        config = ConfigParser.ConfigParser()
        config.readfp(open(config_file))

        # connection settings
        self.url =  str(config.get('redis connection', 'url'))
        self.port = int(config.get('redis connection', 'port'))
        self.password = str(config.get('redis connection', 'password'))

        # loop handler settings
        self.iterations = int(config.get('loop', 'iterations'))
        self.value_multiplier = int(config.get('loop', 'value_multiplier'))
        self.print_iter = int(config.get('loop', 'print_iter'))

class MaxOut():
    def __init__(self, config):
        self.url = config.url
        self.port = config.port
        self.password = config.password
        self.iterations = config.iterations
        self.value_multiplier = config.value_multiplier
        self.print_iter = config.print_iter
        self.connect()

    def connect(self):
        self.r_server = redis.Redis(self.url,
            port = self.port,
            password = self.password)

    def validate_config(self):
        # TODO check connection
        # TODO check loop config

        # FIXME stub
        return True

    def flush(self):
        self.r_server.flushall()

    def max_out(self):
        if(not self.validate_config()):
            print 'exiting...invalid configuration'
            return

        for x in range(0, self.iterations):
            m = hashlib.md5()
            my_date = datetime.datetime.today()
            m.update(str(my_date))
            value = str(m.hexdigest()) * self.value_multiplier
            self.r_server.set(my_date, value)

            if(x % self.print_iter == 0):

                redis_memory_used = self.r_server.info()['used_memory']
                print str(x) + ": " + str(redis_memory_used) + " bytes"

max_out_config = MaxOutConfig()
redisTorture = MaxOut(max_out_config)
redisTorture.flush()
redisTorture.max_out()
