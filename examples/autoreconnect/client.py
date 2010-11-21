#! /usr/bin/env python
import sys, time
import Pyro.naming, Pyro.core
from Pyro.protocol import getHostname

# initialize the client and set the default namespace group
Pyro.core.initClient()

# locate the NS
locator = Pyro.naming.NameServerLocator()
print 'Searching Naming Service...',
ns = locator.getNS()

print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

URI=ns.resolve(':test.autoreconnect')
obj = Pyro.core.getAttrProxyForURI(URI)

while 1:
	print 'call...'
	try:
		obj.method(42)
		print 'Sleeping 1 second'
		time.sleep(1)
		#obj._release() # experiment with this
		#print 'released'
		#time.sleep(2)
	except Pyro.errors.ConnectionClosedError,x:     # or possibly even ProtocolError
		print 'Connection lost. REBINDING...'
		print '(restart the server now)'
		obj.adapter.rebindURI(tries=10)

