#############################################################################
#
#	$Id: util2.py,v 2.2 2004/02/04 23:27:00 irmen Exp $
#	Pyro Utilities (part 2, to avoid circular dependencies)
#	User code should never import this, always use Pyro.util!
#
#	This is part of "Pyro" - Python Remote Objects
#	which is (c) Irmen de Jong - irmen@users.sourceforge.net
#
#############################################################################

def supports_multithreading():
	try:
		from threading import Thread, Lock
		return 1
	except:
		return 0
	
def supports_compression():
	try:
		import zlib; return 1
	except:
		return 0

if supports_multithreading():
	import threading
