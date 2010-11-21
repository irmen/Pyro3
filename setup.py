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
		long_description = """Pyro stands for PYthon Remote Objects. It is an advanced and powerful Distributed Object Technology system written entirely in Python, that is designed to be very easy to use.""",
		author = "Irmen de Jong",
		author_email="irmen@razorvine.net",
		keywords="distributed objects, middleware, network communication, DOT, RMI, IPC",
		url = "http://www.xs4all.nl/~irmen/pyro3/",
		download_url="http://www.xs4all.nl/~irmen/pyro3/download/",
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
		        "Programming Language :: Python :: 2.5",
		        "Programming Language :: Python :: 2.6",
		        "Topic :: Software Development :: Object Brokering",
		        "Topic :: System :: Distributed Computing",
		        "Topic :: System :: Networking"
		    ]
	)
