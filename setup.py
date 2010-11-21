#!/usr/bin/env python
#
# $Id: setup.py,v 2.26 2005/05/26 21:25:14 irmen Exp $
# Pyro setup script
#

from distutils.core import setup
import sys,os

from ConfigParser import ConfigParser

def gather_scripts():
	names = ['es', 'genguid', 'ns', 'nsc', 'rns', 'xnsc', 'wxnsc' ]
	if sys.platform == 'win32':
		names.extend(['nssvc','essvc']) # scripts that are only for Windows
		names = map( lambda x: x+'.bat', names)
	else:
		names.extend(['esd', 'nsd']) # scripts that are not for Windows
	names = map( lambda x: os.path.join( 'bin', x), names )
	return names

if __name__ == '__main__' :
	if not sys.argv[1].startswith('install'):
		scripts=gather_scripts()
	else:	
		print 'This script will install Pyro on your system.'
		# first, confirm the installation path of the scripts.
		scripts=[]
		config='setup.cfg'
		cp=ConfigParser()
		cp.read(config)
		if cp.has_option('install-options','unattended'):
			unattended=cp.get('install-options','unattended')
		else:	
			unattended=0
		if unattended:
			scr='y'
			loc=cp.get('install','install-scripts')
			print 'Unattended install. Scripts will go to',loc
		else:
			scr=raw_input('Do you want the Pyro scripts (in bin/) installed (y/n)? ')

		if scr.lower()=='y':
			#loc=cp.get('install','install-scripts')
			if unattended:
				scr=None
			else:	
				print 'Some Pyro scripts may conflict with system tools already on your system.'
				print 'Choose your script install directory carefully.'
				print 'The default location is usually something like C:\\Python\\Scripts'
				print 'on Windows and /usr/local/bin on Unixes.'
				#scr=raw_input('Where do you want them to be installed ('+loc+')? ')
				scr=raw_input('Where do you want them to be installed (empty=default loc.)? ')

			if scr:
				loc=scr
				if not cp.has_section('install'):
					cp.add_section('install')
				cp.set('install','install-scripts',loc)
				cp.write(open(config,'w'))
				print 'Your scripts are going to be installed into ',loc
			elif not unattended:
				cp.remove_section('install')
				cp.write(open(config,'w'))
				print 'Your scripts are going to be installed into the default location.'
				loc = 'the default location.'

			scripts=gather_scripts()
			print "SCRIPTS=",scripts

			print
		else:
			print 'For maximum comfort, don\'t forget to install the script tools in bin/ yourself ;-)'
			print

	# extract version string from Pyro/constants.py
	ver=open(os.path.join('Pyro','constants.py'),'r').read()
	ver=ver[ver.find('VERSION'):].split('\'')[1]
	print 'Pyro Version = ',ver

	setup(name="Pyro",
		version= ver,
		license="MIT",
		description = "Powerful but easy-to-use distributed object middleware for Python",
		author = "Irmen de Jong",
		author_email="irmen@users.sourceforge.net",
		url = "http://pyro.sourceforge.net/",
		long_description = """Pyro is an acronym for PYthon Remote Objects. It is an advanced and powerful Distributed Object Technology system written entirely in Python, that is designed to be very easy to use. It resembles Java's Remote Method Invocation (RMI). It has less similarity to CORBA - which is a system- and language independent Distributed Object Technology and has much more to offer than Pyro or RMI. But Pyro is small, simple and free!""",
		packages=['Pyro','Pyro.EventService','Pyro.ext'],
		scripts = scripts,
		platforms='any'
	)
    
	if sys.argv[1].startswith('install'):
		if not unattended:
			if scripts:	
				print
				print 'Your scripts have been installed into ',loc
				print 'Please add this directory to your PATH (if it\'s not there already)'
			else:	
				print
				print 'For maximum comfort, don\'t forget to install the script tools in bin/ yourself ;-)'
			print 'And, place the manual (in docs/) somewhere for easy reference!'
			print
		else:
			print 'Install finished.'

