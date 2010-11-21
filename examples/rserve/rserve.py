import Pyro.errors
import Pyro.ext.remote as remote
import UserDict

Pyro.config.PYRO_MULTITHREADED  = 0
Pyro.config.PYRO_MAXCONNECTIONS = 1000

def connect(host):
	return remote.get_remote_object('rserver', host, None)

def copied(cls = None):
	if cls is None:
		remote.copy_types = 1
	else:
		remote.register_type(cls)

def serve(wait_time = None, callback = None):
	return remote.handle_requests(wait_time, callback)

def close():
	pass
