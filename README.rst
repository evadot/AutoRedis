AutoRedis
=========

AutoRedis execute the redis command on the appropriate server (master of slave) depending on if the commands writes data or not.

If the command write data (like set) it will be automatically done on the master.

If the command reads data (like get) it will be automatically done on one of the slave with a fallback on the master if no slaves are up or configured.

See the examples directory for complete examples.
