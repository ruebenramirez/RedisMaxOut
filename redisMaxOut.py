#!/usr/bin/python

import os
import datetime
import hashlib

import redis


class MaxOutConfig():
    def __init__(self):
        self.read_config()

    def read_config(self):
        # connection settings
        self.host = os.environ['REDIS_MAXOUT_HOST']
        self.port = os.environ['REDIS_MAXOUT_PORT']
        self.password = os.environ['REDIS_MAXOUT_PASSWORD']

        # TODO: do we even need these?
        # loop handler settings
        self.iterations = os.environ['REDIS_MAXOUT_LOOP_ITERATIONS']
        self.value_multiplier = os.environ['REDIS_MAXOUT_LOOP_VALUE_MULTIPLIER']
        self.print_iter = os.environ['REDIS_MAXOUT_LOOP_PRINT_ITER']

        # check config settings
        self.validate_config()

    def validate_config(self):
        if self.host is None:
            raise Exception('Please specify a Redis host')
        if self.port is None:
            raise Exception('Please specify a Redis port')
        if not self.port.isdigit():
            raise Exception('Please specify numeric Redis port')


class MaxOut():
    def __init__(self, config):
        self.host = config.host
        self.port = config.port
        self.password = config.password
        self.iterations = config.iterations
        self.value_multiplier = config.value_multiplier
        self.print_iter = config.print_iter
        self.connect()

    def connect(self):
        self.r_server = redis.Redis(self.host, port=self.port,
                                    password=self.password)

    def flush(self):
        self.r_server.flushall()

    def max_out(self):
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
