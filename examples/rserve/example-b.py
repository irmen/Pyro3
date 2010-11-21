import rserve
import exlib
import sys

if len(sys.argv)==2:
	hostname=sys.argv[1]
else:
	hostname=None
dict = rserve.connect(hostname)

dict.log("connection from example-b")

myobj = dict["foo"]
print "invoking hello..."
print myobj.hello()

rserve.close()
