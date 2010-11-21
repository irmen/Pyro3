import Pyro.core
import Pyro.naming
import time

ns_uri=Pyro.naming.NameServerLocator().getNS().URI
print "Name server location:",repr(ns_uri)

print "Timing raw rebind (connect) speed..."
proxies=[Pyro.core.DynamicProxy(ns_uri) for i in range(10)]
for p in proxies:
	p.ping()
begin=time.time()
ITERATIONS=100
for loop in xrange(ITERATIONS):
	if loop%10==0:
		print loop*len(proxies)
	for p in proxies:
		p._release()
		p.adapter.rebindURI()
duration=time.time()-begin
print "%d connections in %s sec = %f conn/sec" % (ITERATIONS*len(proxies), duration, ITERATIONS*len(proxies)/duration)
del proxies

print "Timing proxy connect speed..."
ITERATIONS=1000
begin=time.time()
for loop in xrange(ITERATIONS):
	if loop%100==0:
		print loop
	p=Pyro.core.DynamicProxy(ns_uri)
	p.ping()
duration=time.time()-begin
print "%d new proxy calls in %s sec = %f calls/sec" % (ITERATIONS, duration, ITERATIONS/duration)
