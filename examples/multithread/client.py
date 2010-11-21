#! /usr/bin/env python
import sys, os

import time


sys.path.insert(0,os.pardir)	# to find testclient.py

import testclient

count = int(raw_input('Number of parallel clients: '))


test = testclient.getproxy('multithread')

testObjects=[test]

for i in range(count-1):
	testObjects.append(test.__copy__())

processtime = 1.0

def processing(name, proxy):
	print 'Processing started',name
	while 1:
		t1 = time.time()
		print name, "CALLING...."
		print name, proxy.process(name,processtime),
		span = time.time() - t1
		print 'It took %.2f sec' % span


# start a set of child processes which perform requests

print
print 'I will create a set of child processes which run concurrently.'
print 'Each process invokes the remote object with a process time of',processtime,'seconds.'
print 'The remote object will wait that long before completion.'
print 'If the remote server is singlethreaded, each invocation is processed sequentially and has to wait for the previous one to complete. This will result in processing times longer than the specified amount!'
print 'If the remote server is multithreaded, all remote invocations are processed in parallel and will complete exactly after the specified process time.'

childs=[]

for i in range(count):
	pid = os.fork()		# XXX doesn't work on windows!
	if pid:
		childs.append(pid)
	else:
		time.sleep(count-i)
		processing('Process%d' % (i+1), testObjects[i])
		_exit(0)

void=raw_input('\nPress enter to stop...\n\n')
for p in childs:
	os.kill(p,1) # SIGHUP
	print 'killed',os.wait()
print 'Graceful exit.'

