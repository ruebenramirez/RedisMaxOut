#!/usr/bin/python

from sys import argv
import ConfigParser, os
import redis
import datetime
import hashlib

class MaxOutConfig():
    def __init__(self):
        self.readConfig()
    
    def readConfig(self): 
        try:
            configFile = argv[1]
        except IndexError:
            configFile = 'setup.cfg'

        config = ConfigParser.ConfigParser()
        config.readfp(open(configFile))

        # connection settings
        self.url =  config.get('redis connection', 'url')
        self.port = config.get('redis connection', 'port')
        self.password = config.get('redis connection', 'password')

        # loop handler settings
        self.iterations = int(config.get('loop', 'iterations'))
        self.valueMultiplier = int(config.get('loop', 'valueMultiplier'))
        self.printIter = int(config.get('loop', 'printIter'))

class RedisMaxOut():

    def __init__(self, config):
        # TODO if no config, then bail
        self.url = config.url
        self.port = config.port
        self.password = config.password
        self.iterations = config.iterations
        self.valueMultiplier = config.valueMultiplier
        self.printIter = config.printIter
        self.connect()

    def connect(self):
        self.r_server = redis.Redis(self.url,
            port = self.port,
            password = self.password)

    def validateConfig(self):
        # TODO check connection
        # TODO check loop config

        # FIXME stub
        return True

    def flushOld(self):
        self.r_server.flushall()

    def maxOut(self):
        if(not self.validateConfig()):
            print 'exiting...invalid configuration'
            return

        for x in range(0, self.iterations):
            m = hashlib.md5()
            myDate = datetime.datetime.today()
            m.update(str(myDate))
            value = str(m.hexdigest()) * self.valueMultiplier
            self.r_server.set(myDate, value)

            if(x % self.printIter == 0):
                print str(x) + ": " + str(self.r_server.get(x))

                redisMemoryUsed = self.r_server.info()['used_memory']
                print "memory used: " + str(redisMemoryUsed)

maxOutConfig = MaxOutConfig()
redisTorture = RedisMaxOut(maxOutConfig)
redisTorture.flushOld()
redisTorture.maxOut()

# def main():

# if __name__ == "__main__:":
    # main()
