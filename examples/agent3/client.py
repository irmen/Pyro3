#! /usr/bin/env python
import sys, os

from Pyro.errors import *
import Pyro.core

sys.path.insert(0,os.pardir)	# to find testclient.py

import testclient

import agent.ShoppingAgent as SA

Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code

# Get a proxy with attrs 
mall = testclient.getproxy('Shop1',True)

import sys, os, string
import Pyro.core

Harry = SA.ShoppingAgent('Harry')
Joyce = SA.ShoppingAgent('Joyce')

try:
	print 'Harry goes shopping...'
	Harry=mall.goShopping(Harry)		# note that agent returns as result value
	Harry.result()
	print
	print 'Joyce goes shopping...'
	Joyce=mall.goShopping(Joyce)		# note that agent returns as result value
	Joyce.result()
	print
except Exception,x:
	import Pyro.util
	print ''.join(Pyro.util.getPyroTraceback(x))
