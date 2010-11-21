#!/usr/bin/env python
#
# $Id: setup.py,v 2.26.2.5 2009/11/27 23:49:32 irmen Exp $
# Pyro setup script
#

from distutils.core import setup
import sys,os,glob
import sets


if __name__ == '__main__' :
	scripts=sets.Set(glob.glob("bin/pyro-*.cmd"))
	if sys.platform != 'win32':
		scripts=sets.Set(glob.glob("bin/pyro-*")) - scripts
	
	# extract version string from Pyro/constants.py
	code=compile(open(os.path.join('Pyro','constants.py')).read(), "constants", "exec")
	constants={}
	exec code in constants
	version=constants["VERSION"]
	print 'Pyro Version =',version

	setup(name="Pyro",
		version= version,
		license="MIT",
		description = "distributed object middleware for Python (IPC/RPC)",
		long_description = """Pyro is an acronym for PYthon Remote Objects. It is an advanced and powerful Distributed Object Technology system written entirely in Python, that is designed to be very easy to use. It resembles Java's Remote Method Invocation (RMI). It has less similarity to CORBA - which is a system- and language independent Distributed Object Technology and has much more to offer than Pyro or RMI. But Pyro is small, simple and free!""",
		author = "Irmen de Jong",
		author_email="irmen@users.sourceforge.net",
		keywords="distributed objects, middleware, network communication, DOT, RMI, IPC",
		url = "http://pyro.sourceforge.net/",
		download_url="http://downloads.sourceforge.net/project/pyro/Pyro/"+version+"/Pyro-"+version+".tar.gz?use_mirror=autoselect",
		packages=['Pyro','Pyro.EventService','Pyro.ext'],
		scripts = list(scripts),
		platforms="any",
		classifiers=[
		        "Development Status :: 5 - Production/Stable",
		        "Development Status :: 6 - Mature",
		        "Intended Audience :: Developers",
		        "License :: OSI Approved :: MIT License",
		        "Operating System :: OS Independent",
		        "Programming Language :: Python",
		        "Topic :: Software Development :: Object Brokering",
		        "Topic :: System :: Distributed Computing",
		        "Topic :: System :: Networking"
		    ]
	)
