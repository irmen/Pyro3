import rserve
import exlib
import sys
import Pyro

# Pyro.config.PYRO_PORT = 7780

if len(sys.argv)==2:
	hostname=sys.argv[1]
else:
	hostname=None
dict = rserve.connect(hostname)
dict.log("connection from example-a")

obj = exlib.myobj()
obj.value = 20
dict["foo"] = obj

print "placed object in the distributed dictionary."
rserve.serve()
