This shows how oneway method calls work.
The client uses a oneway call to the server to start
it. In the meantime, it continues by itself and does some
things. After a short while, it uses regular Pyro calls again
to check on the server until it is ready.

Things to notice:
Not only will the client continue immediately after the oneway
method has been called, the server will also process the method
invocation 'in the background'. Other methods may be called while
the oneway call -which takes a while to complete- is still running.

For more information see the Features chapter in the manual
(callbacks & oneway calls).


(Due to a bug in Pyro 3.4 and older, the oneway call is not
processed in the background on the server, and subsequent
method calls must wait. So use 3.5 or newer to see it work
as it was intended)
