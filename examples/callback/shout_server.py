#! /usr/bin/env python
import sys, os
sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver

import Pyro.core, Pyro.util

######## object that does the callbacks

class CallbackThing(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		self.clients=[]
		self.callbackMutex = Pyro.util.getLockObject()
	def register(self, client):
		print 'REGISTER',client
		self.clients.append(client)
		#client._setOneway('callback') # don't wait for results for this method
	def shout(self, message):	
		print 'Got shout:',message
		# let it know to all clients!
		for c in self.clients[:]:		# use a copy of the list
			try:
				self.callbackMutex.acquire()
				try:
					# claim the proxy for ourselves.
					# we can do this now because we are in a thread mutex.
					c._transferThread()
					c.callback('Somebody shouted: '+message) # oneway call
				finally:
					self.callbackMutex.release()
			except Pyro.errors.ConnectionClosedError,x:
				# connection dropped, remove the listener if it's still there
				# check for existence because other thread may have killed it already
				if c in self.clients:
					self.clients.remove(c)
					print 'Removed dead listener',c


######## main program

testserver.start(CallbackThing,'callback')

