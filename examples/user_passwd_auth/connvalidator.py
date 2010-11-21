from Pyro.protocol import DefaultConnValidator
import Pyro.constants
import md5, hmac


# Example username/password database:
EXAMPLE_ALLOWED_USERS = {
	"irmen": "secret",
	"guest": "guest",
	"root": "change_me",
}

#
#	Example login/password validator.
#	Passwords are protected using md5 so they are not stored in plaintext.
#	The actual identification check is done using a hmac-md5 secure hash.
#
class UserLoginConnValidator(DefaultConnValidator):

	def _xform(self, s):
		return md5.new(s).digest()	# use md5 hash instead of plaintext

	def acceptIdentification(self, daemon, connection, token, challenge):
		login, password = token.split(':', 1)
		realpass = EXAMPLE_ALLOWED_USERS.get(login)
		# Check if the username/password is valid.
		if realpass and hmac.new(challenge,self._xform(realpass)).digest() == password:
			print "ALLOWED", login
			connection.authenticated=login  # store for later reference by Pyro object
			return(1,0)
		print "DENIED",login
		return (0,Pyro.constants.DENIED_SECURITY)
		
	def createAuthToken(self, authid, challenge, peeraddr, URI, daemon):
		return "%s:%s" % (authid[0], hmac.new(challenge,authid[1]).digest() )

	def mungeIdent(self, ident):
		# ident is tuple (login, password), the client sets this.
		return (ident[0], self._xform(ident[1]))
		
