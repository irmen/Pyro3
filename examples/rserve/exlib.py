import rserve
import sys

class myobj:
	value = 10
	def hello(self):
		print "Hello, world", self.value
		return "I said 'hello world'..."
