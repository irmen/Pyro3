#! /usr/bin/env python
import Pyro.naming
import Pyro.core
import chain

Pyro.core.initServer()

daemon = Pyro.core.Daemon()
ns = Pyro.naming.NameServerLocator().getNS()
daemon.useNameServer(ns)

objName='B'
nextName='C'

daemon.connect(chain.Chain(objName,nextName),':test.chain_'+objName)

# enter the service loop.
print 'Server started obj',objName
daemon.requestLoop()

