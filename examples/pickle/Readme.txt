This test contains a quite detailed test of the ability of various key Pyro
objects to be pickled. Especially the proxy objects need to work flawlessly.
The program repeats the test for every available pickle protocol level.
There should be zero errors at the end.
The test requires a name server to be up and running.
