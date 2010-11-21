This test is to find out the average time it takes for a remote
PYRO method call. Also it is a kind of stress test because lots
of calls are made in a very short time.

The oneway method call test is very fast if you run the client 
and server on different machines. If they're running on the same
machine, the speedup is less noticable.
