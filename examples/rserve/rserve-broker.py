#!/usr/bin/python

import Pyro.errors
import Pyro.ext.remote as remote
import os.path
import socket
import string
import sys
import types
import UserDict

Pyro.config.PYRO_MULTITHREADED  = 0
Pyro.config.PYRO_MAXCONNECTIONS = 1000

from getopt import getopt

options = [
	"compress",
	"help",
	"host=",
	"port=",
	"ns-port=",
	"log-file=",
	"script=",
	"verbose",
]

(opts, args) = getopt(sys.argv[1:], [], longopts = options)
true, false = 1, 0

host       = socket.gethostbyname(socket.gethostname())
port       = None
ns_port    = None
ident      = 'rserver'
log_file   = None
verbose    = false

def usage():
	print """
Welcome to the rserve-broker program.  Command syntax is:

  %s [options [args] ...] <name of server module>

Possible options are:

  --help               Show this page
  --log-file FILE      Output logging information into FILE
  --host NAME          Export objects using hostname NAME
  --port NUMBER        Export objects using port PORT
  --verbose            Generate verbose output; for debugging only
  --compress           Compress transmissions to the client
""" % os.path.basename(sys.argv[0])
	sys.exit(0)

for opt in opts:
	if opt[0] == "--help":
		usage()
	elif opt[0] == "--host":
		host = opt[1]
	elif opt[0] == "--port":
		port = int(opt[1])
	elif opt[0] == "--ns-port":
		ns_port = int(opt[1])
	elif opt[0] == "--verbose":
		verbose = true
	elif opt[0] == "--compress":
		Pyro.config.PYRO_COMPRESSED = true
	elif opt[0] == "--log-file":
		log_file = opt[1]

######################################################################
###
### Start a Pyro naming service on the host
###

import Pyro.naming
import threading

# check if a Name server already exists, if not, start our own
try:
	ns = remote.Nameserver(host, ns_port)
	ns.resolve("foo")
except remote.Error:
	pass
except Pyro.errors.PyroError:
	starter = Pyro.naming.NameServerStarter()
	threading.Thread(target = starter.start, args   = (host, ns_port)).start()
	starter.waitUntilStarted() # make sure the name server is started!


######################################################################
###
### Create the server object
###
ns = remote.Nameserver(host, ns_port)

class Server(UserDict.UserDict):
	"The Server is a plain dictionary for now, with no security."
	def __init__(self, log, ns):
		self.log_file   = log
		self.nameserver = ns
		UserDict.UserDict.__init__(self)

	def __nonzero__(self): return 1

	def __hash__(self):
		return 1234;

	def add(self, key, obj):
		UserDict.UserDict.__setitem__ (self, key, obj)

	def log(self, msg):
		print msg

server = Server(log_file, ns)

######################################################################
###
### Provide the server via the Pyro nameserver, under the name
### `server'
###

remote_ready = false

server.log("Providing server object")

remote.daemon_host = host
remote.daemon_port = port
remote.verbose     = verbose

# Register the significant base type, derivatives of which should
# always be wrapped during and after transport to remote sites
#remote.register_type(Object)

try:
	ns.register(ident, server)
	remote_ready = true
except Pyro.errors.PyroError, msg:
	server.log(msg)
	server = None
	sys.exit(1)

######################################################################
###
### Loop, waiting for connections
###

if remote_ready:
	server.log("Server is now ready")
	status = remote.handle_requests(1800)
	server.log("Server has shutdown")
	server = None
else:
	server.log("Remote not ready; shutting down")
	status = 1

sys.exit(status)
