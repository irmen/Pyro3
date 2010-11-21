import agent.base   # use fully qualifed module name. "import base" doesn't work with mobile code.

class ShoppingAgent(agent.base.Agent):
    def __init__(self, name):
        agent.base.Agent.__init__(self)
        self.name=name
        self.visited=[]
    def result(self):
        print 'My name is',self.name
        print 'I have visited',self.visited
    def visit(self, name):
        self.visited.append(name)
    def __str__(self):
        return self.name
        

