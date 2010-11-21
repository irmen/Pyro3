#! /usr/bin/env python

import Pyro.util
import Pyro.core
import threading
import time
import copy

def myThread(proxy):
	print "inside myThread().. calling mul...:",
	try:
		print proxy.mul(222,10)
	except Exception,x:
		print ">>Exception in myThread:",x
	print "done in myThread()."


Pyro.core.initClient()

test = Pyro.core.getAttrProxyForURI("PYRONAME://:test.simple")

print "Got a new proxy, first call is from a different thread (should work!)"
thread=threading.Thread(target=myThread, args=(test,) )
thread.start()
time.sleep(1)
print "Now calling it from main thread (should fail)"
try:
	print test.mul(111,9)
except Exception,x:
	print "(expected) exception:",x

# create a copy of the proxy and use that instead. Should work.
print "Calling a copy of the proxy, that should work."
test2 = copy.copy(test)
print test2.mul(111,9)

# release the original proxy, and try again.
# this time it should work, because it is us that reconnect it...
print "releasing original proxy and calling again (should work now)"
test._release()
print test.mul(111,9)



# do again from a thread. This should fail now
print "Calling from a thread. Should now get exception about proxy sharing!"
thread=threading.Thread(target=myThread, args=(test,) )
thread.start()
time.sleep(1)

# do again from a thread, but this time transfer ownership
# after that, when *we* attempt to call it it should fail instead... :)
print "\nCall again from a thread, but with thransfered ownership. No exception should occur this time."
print "Transfer ownership to thread..."
thread=threading.Thread(target=myThread, args=(test,) )
test._transferThread(thread)  # usually, the thread itself calls this.
thread.start()  # should work now
time.sleep(1)

print "\n\ncalling ourselves again...(should get exception now):"
print test.mul(44,55)    # should fail now

print "end"
