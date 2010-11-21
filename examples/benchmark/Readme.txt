This test is to find out the average time it takes for a remote
PYRO method call. Also it is a kind of stress test because lots
of calls are made in a very short time.

Since Pyro 3.0, performance doesn't really suffer if your server
is running in multithreaded mode. It should be as fast as
singlethreaded mode.
