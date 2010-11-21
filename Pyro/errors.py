#############################################################################
#
#	$Id: errors.py,v 2.15 2005/02/12 23:45:29 irmen Exp $
#	Pyro Exception Types
#
#	This is part of "Pyro" - Python Remote Objects
#	which is (c) Irmen de Jong - irmen@users.sourceforge.net
#
#############################################################################


#############################################################################
# PyroError is the Pyro exception type which is used for problems WITHIN Pyro.
# User code should NOT use it!!
#
# NOTE: Any exception occuring in the user code on the server will be catched
# and transported to the client, where it is raised just as if it occured
# locally. The occurrence is logged in the server side Pyro log.
# Pyro will use the [Remote]PyroError exceptions and their subtypes to
# indicate that an internal problem occured.
#############################################################################

class PyroError(Exception):     pass		# internal

class URIError(PyroError):      pass		# URI probs
class DaemonError(PyroError):   pass		# daemon probs
class ProtocolError(PyroError): pass		# protocol adapter
class ConnectionClosedError(ProtocolError): pass	# connection in adapter is closed
class ConnectionDeniedError(ProtocolError): pass	# server refused connection
class TimeoutError(ConnectionClosedError): pass		# communication timeout
class NamingError(PyroError):   pass		# name server
class NoModuleError(PyroError):	pass		# no module found for incoming obj

# do NOT use the following yourself:
class _InternalNoModuleError(PyroError):	
	def __init__(self, modulename, fromlist, *args):
		PyroError.__init__(* (self,)+args)
		self.modulename=modulename
		self.fromlist=fromlist


#############################################################################
#	Remote exception printing
#############################################################################

import types, constants

def __excStr__(selfobj) :
	# This method replaces __str__ method of exception classes in order to
	# return the remote traceback with the current message
	
	remote_tb = getattr(selfobj,constants.TRACEBACK_ATTRIBUTE,None)

	if remote_tb:
		std_str = selfobj.standardStr()
		ztr = std_str
		ztr += "\n  This exception occured remotely (Pyro) - Remote traceback:"
		
		for line in remote_tb :
			if line.endswith("\n"):
				line=line[:-1]
				
			lines = line.split("\n")
			for line in lines :
				ztr += "\n  | %s" % line

		ztr += "\n  +--- End of remote traceback"
		return ztr
			
	else:
		# It's not a remote exception - Return the standard string
		# (the exception class is permanently patched!)
		return selfobj.standardStr()


#############################################################################
#
#	PyroExceptionCapsule - Exception encapsulation.
#
#	This class represents a Pyro exception which can be transported
#	across the network, and raised on the other side (by invoking raiseEx).
#	NOTE: the 'real' exception class must be 'known' on the other side!
#	NOTE2: this class is adapted from exceptions.Exception.
#	NOTE3: PyroError IS USED FOR ACTUAL PYRO ERRORS. PyroExceptionCapsule
#          IS ONLY TO BE USED TO TRANSPORT AN EXCEPTION ACROSS THE NETWORK.
#	NOTE4: It sets a special attribute on the exception that is raised
#	       (constants.TRACEBACK_ATTRIBUTE), this is the *remote* traceback 
#   NOTE5: ---> this class is intentionally not subclassed from Exception!!!
#          Pyro's exception handling depends on this!
#
#############################################################################

class PyroExceptionCapsule:
	def __init__(self,excObj,args=None):
		self.excObj = excObj
		self.args=args  # if specified, this is the remote traceback info
	def raiseEx(self):
		import Pyro.constants
		# Modify __str__ method of exception class to append the remote traceback to the error message
		# Normally self.excObj is an exception class (if server maps "string exceptions" to normal exceptions)
		if type(self.excObj) == types.InstanceType :
			excClass = self.excObj.__class__
			if Pyro.config.PYRO_PRINT_REMOTE_TRACEBACK:
				try :
					Pyro_warning = excClass.Pyro_warning
				# If no exception : exception class already patched
				except :
					excClass.Pyro_warning = "Method __str__ has been remapped to accomodate remote traceback display (old __str__ is now standardStr)"
					excClass.standardStr = excClass.__str__
					excClass.__str__ = __excStr__
			else:
				excClass.standardStr=excClass.__str__

		setattr(self.excObj,Pyro.constants.TRACEBACK_ATTRIBUTE,self.args)
		raise self.excObj
	def __str__(self):
		s=self.excObj.__class__.__name__
		if not self.args:
			return s
		elif len(self.args) == 1:
			return s+': '+str(self.args[0])
		else:
			return s+': '+str(self.args)
	def __getitem__(self, i):
		return self.args[i]	

