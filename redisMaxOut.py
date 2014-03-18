# maximize the key usage

import redis
import hashlib
import datetime

url = "<instanceName>.redistogo.com"
port = <port>
password = "<password>"

def connect(url, port, password):
    r_server = redis.Redis(url,
        port = port,
        password = password)
    return r_server

def maxOut(r_server,
        min = 0,
        max = 900000,
        valueMultiplier = 20,
        printIter = 100):

    for x in range(min, max):
        m = hashlib.md5()
        myDate = datetime.datetime.today()
        m.update(str(myDate))
        value = str(m.hexdigest()) * valueMultiplier
        r_server.set(myDate, value)

        if(x % printIter == 0):
            print str(x) + ": " + str(r_server.get(x))

            memoryUsed = r_server.info()['used_memory']
            print "memory used: " + str(memoryUsed)

r = connect(url, port, password)
maxOut(r)
