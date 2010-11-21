#
#	Test client utility startup code
#

import sys
import Pyro.naming, Pyro.core, Pyro.protocol

group = ':test'  # the default namespace group for the tests

# objname = the name of the object which is used in the NS
# withAttrs = use a DynamicProxyWithAttrs or a regular DynamicProxy?
def getproxy(objName, withAttrs=0):
	# initialize the client and set the default namespace group
	Pyro.core.initClient()
	Pyro.config.PYRO_NS_DEFAULTGROUP=group

	# locate the NS
	locator = Pyro.naming.NameServerLocator()
	print 'Searching Naming Service...',
	ns = locator.getNS()
	print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

	# resolve the Pyro object
	print 'binding to object'
	try:
		URI=ns.resolve(objName)
		print 'URI:',URI
	except Pyro.core.PyroError,x:
		print 'Couldn\'t bind object, nameserver says:',x
		raise SystemExit

	# create a proxy for the Pyro object, and return that
	if withAttrs:
		return Pyro.core.getAttrProxyForURI(URI)
	else:
		return Pyro.core.getProxyForURI(URI)

