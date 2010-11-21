This test shows a real (2-way!) mobile 'agent' system. 

That is, the server doesn't have the agent code (python module)
available and will download it from the client!
The server is in the "serv" directory, and you can see that
there is no ShoppingAgent.py module there. Only the client has it.

As soon as the client sends a ShoppingAgent to the server, the
server reports back that it doesn't have the code. The client then
uploads the module to the server and the program continues just
as if the module could be loaded after all.

Notice that this happens IN PYRO; the server only has to enable
the mobile code feature. In this case it also installs a codeValidator
because the default codeValidator accepts ALL INCOMING CODE.

The client doesn't have to do anything special to make this work.

FURTHERMORE: the agent brings back actual objects from the server that
were previously unknown on the client! The mobile code feature works
both ways. The client can *download* code from the server too!
What you see when the client "describes the objects she's bought" are
the descriptions that the objects downloaded from the server return.
(you can see those objects in the serv/objects directory. The client
has no access to this module, just as the server has no access to the
client's 'agent' module).


NOTE that once the code is downloaded on the server, it stays there.
It is not downloaded again. So there is a possible version control issue here.
If the server keeps running and the client has updated its agent code in
the meantime, the server will not notice this, and it will continue to use
the previous (old) agent code.

ALSO NOTE that due to a limitation of Python and the current mobile code
implementation in Pyro, your agents *must* be located in a separate 
module. Any agents declared in the module that runs as __main__ will not work!

