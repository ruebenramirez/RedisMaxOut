RedisMaxOut
===========

max out redis memory store to test max memory key eviction policy settings

###Configure via Setup.cfg

1. copy example.setup.cfg to setup.cfg
1. update the connection details
1. modify the loop config details to tweak the iteration count and value size assigned to each key

###TODO

* add more exception handling and clean up the run to make it a usable tool
* report on redis configuraiton as an option
* change redis configuration settings (e.g. eviction policy, eviction sample size, etc.)
* simulate redis usage scenarios: blowout, linear increase, exponential increase, variable pattern, high/medium/low trigger patterns, etc.)
* provide metrics on the run (key eviction accuracy in max memory scenarios)
* ready this tool to test cluster configurations
* add support for expires on some/all keys
