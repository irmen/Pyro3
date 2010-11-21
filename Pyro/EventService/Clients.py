#############################################################################
#  
#	$Id: Clients.py,v 2.15 2005/01/22 01:05:43 irmen Exp $
#	Event Service client base classes
#
#	This is part of "Pyro" - Python Remote Objects
#	which is (c) Irmen de Jong - irmen@users.sourceforge.net
#
#############################################################################

import Pyro.core, Pyro.naming, Pyro.constants
import Pyro.EventService.Server
from Pyro.errors import *

# SUBSCRIBER: subscribes to certain events.
class Subscriber(Pyro.core.CallbackObjBase):
	def __init__(self, ident=None):
		Pyro.core.CallbackObjBase.__init__(self)
		Pyro.core.initServer()
		Pyro.core.initClient()
		daemon = Pyro.core.Daemon()
		locator = Pyro.naming.NameServerLocator(identification=ident)
		self.NS = locator.getNS(host=Pyro.config.PYRO_NS_HOSTNAME)
		daemon.useNameServer(self.NS)
		daemon.connect(self)  #  will also set self.daemon...
		uri = self.NS.resolve(Pyro.constants.EVENTSERVER_NAME)
		self.eventservice=Pyro.core.getProxyForURI(uri)
		self.eventservice._setIdentification(ident)
		self.abortListen=0
		self.daemon=daemon	# make sure daemon doesn't get garbage collected now

	def subscribe(self,subjects):
		# Subscribe to one or more subjects.
		# It is safe to call this multiple times.
		self.eventservice.subscribe(subjects, self.getProxy())
	def subscribeMatch(self,subjectPatterns):
		# Subscribe to one or more subjects (by pattern)
		# It is safe to call this multiple times.
		self.eventservice.subscribeMatch(subjectPatterns, self.getProxy())
	def unsubscribe(self, subjects):
		# Unsubscribe the subscriber for the given subject(s).
		self.eventservice.unsubscribe(subjects, self.getProxy())

	def abort(self):
		self.abortListen=1

	def setThreading(self, threaded):
		self.getDaemon().threaded=threaded

	def listen(self):
		self.getDaemon().requestLoop(lambda s=self: not s.abortListen)

	def event(self, event):					# callback, override this!
		print event

# PUBLISHER: publishes events.
class Publisher:
	def __init__(self, ident=None):
		Pyro.core.initClient()
		locator = Pyro.naming.NameServerLocator(identification=ident)
		ns = locator.getNS(host=Pyro.config.PYRO_NS_HOSTNAME)
		uri = ns.resolve(Pyro.constants.EVENTSERVER_NAME)
		self.eventservice=Pyro.core.getProxyForURI(uri)
		self.eventservice._setIdentification(ident)

	def publish(self, subjects, msg):
		self.eventservice.publish(subjects,msg)

