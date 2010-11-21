import Pyro.core
import Pyro.errors
from tasks import md5crack
from tasks import sorting
import time


Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code (for the tasks)

Pyro.core.initClient()

selected_task = raw_input("What task do you want to run (md5 or sorting; m/s): ")

if selected_task in ('m','md5'):
	UIClass = md5crack.UserInterface
	TaskClass = md5crack.CrackTask
elif selected_task in ('s','sorting'):
	UIClass = sorting.UserInterface
	TaskClass = sorting.SortTask
else:
	raise ValueError("invalid task chosen")
		
ui=UIClass()
arguments = ui.begin()
task = TaskClass(arguments)
ui.info(task)
	
choice=input("Do you want sequential/normal (1) or distributed processing (2) ? ")
if choice==1:
	print "(using normal sequential local processing)"
	start=time.time()
	tasks=task.split(3)        # just for the fun of it
	
	while tasks:
		t=tasks.pop()
		print "(local) running task",t
		t.run()
		if task.join(t):
			break
	print "(local) gathering result"
	result=task.getResult()
	duration=time.time()-start

elif choice==2:
	print "(using distributed parallel processing)"
	dispatcher = Pyro.core.getProxyForURI("PYRONAME://:Distributed.Dispatcher")
	start=time.time()
	result=dispatcher.process(task)        # the interesting stuff happens here :)
	duration=time.time()-start
		
ui.result(result)
print "It took %.3f seconds." % duration
