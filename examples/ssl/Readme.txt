This example shows the SSL features of Pyro.

The server is created using the PYROSSL protocol, and will only
accept SSL connections. It installs a connection validator that
prints some info about the client's SSL certificate.

The client code is no different than regular Pyro clients, 
because the Proxy (actually the protocol adapter) knows how
to deal with the PYROSSL: protocol.

Take a peek in the nameserver, you'll see that the server is
registered with a PYROSSL: uri.


The "certs" directory contains a bunch of example certificates.
Make sure that this directory can be found by Pyro.
(the location is specified in the PYROSSL_CERTDIR config item,
which defaults to "certs" in the PYRO_STORAGE directory,
which is by default the current directory).


See m2crypto homepage ( http://sandbox.rulemaker.net/ngps/m2/ ) or openssl
documentation ( http://www.openssl.org ) for instructions on how to
create your own ca and server/client certificates.
Here is a good guide: http://sial.org/howto/openssl/
Important: the creation of the .csr (req) files must be done in a
different directory, with its own host.key. 
The final creation of the server.pem and client.pem file is done by 
concatenating the requester host.key and the .cert file.


NOTE: the demo certificates provided are valid until january 2006.
      At that moment I'll have to create new demo certificates.

