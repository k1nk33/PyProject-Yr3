#!/usr/bin/python

#  Import the twisted methods of Factory, LineReceiver and the Reactor
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

###  Define the main Class and pass the Line receiver as a parameter

class ChatProtocol(LineReceiver):
		
	##  Initialise the Constructor passing the ChatFactory object as an argument
	def __init__(self, factory):
		'''Constructs the instance variables as well as the starting state of new users
		'''
		#  Initialise the instance variables, set our name to None and set our state to New User
		#print('Init')
		self.factory=factory
		self.name=None
		self.state='New User'
		
	##  Reactor receives an incoming connection. Built in Line Receiver method.
	def connectionMade(self):
		'''Function to react to a new connection; sets the initial user state to NewUser
		'''
		#  Check the 'state' of the user, if this is a new user send a welcome message otherwise the user is already registered as active, pass	
		if self.state == 'New User':
			self.sendLine('>>>    An Seo!    <<<') 
	
	#  If the connection breaks down, handle notification and update the user dictionary. Built in Line Receiver method.
	#  Note, 'reason' is an exception variable returned by the protocol
	def connectionLost(self, reason):
		'''This function takes care of any break in connection between server and client
		'''
		#  If the user exists in the user dictionary remove the value associated with them
		if self.name in self.factory.users:
			del self.factory.users[self.name]
			#  Notify all other users of the users departure from the chat, call the broadcastMessage function
			self.broadcastMessage(' >>>   User %s amach sa teach !  <<<'%self.name)
			
	## Function handles the different possible incoming connections, either the user is active and currently chatting so they can be passed to handleChat function
	## or this is a new user in which case they need to be passed to the handle_Register function for processing. Built in Line Receiver method.
	def lineReceived(self, line):
		'''Responsible for controlling the flow of operation, identifies if a client is currently active or if they have just joined
		the chat and then passes them to their relevant handler functions
		'''
		#print('Received')
		#If this instance is a new user pass the line to the handle_Register function, otherwise pass the line to the handle_Chat function.
		if self.state=='New User':
			#print('Registering')
			self.handle_Register(line)
		else:
			#print('Chatting')
			self.handle_Chat(line)
		
	##  Function to register new users
	def handle_Register(self, name):
		'''This function is responsible registering new users
		'''
		#print('Handle reg')
		#  If the name already exists in the user dictionary, ask again. 
		if name in self.factory.users:
			self.sendLine('>>> Username taken! <<<')
			return
		else:
			self.sendLine('OK<')
		#  Otherwise notify other clients of the new client	
		self.broadcastMessage('>>>   User %s AnSeo !   <<<'%name)
		#  Assign the instance variable to the user name received
		self.name=name
		#  Set the current name in the dictionary to represent this instance and set the state to one of a registered user
		self.factory.users[name]=self
		self.state ='CHAT'
	
	##  Function to handle the incoming messages	
	def handle_Chat(self, message):
		'''This function reacts to and also handles the received messages from the client
		'''
		print('Handle chat')
		#  Format the message and store it, once done pass the message to the broadcastMessage function
		message = '>>>%s : %s  <<<'%(self.name, message)
		self.broadcastMessage(message)
	
	##  Function to handle the broadcasting of messages between clients
	def broadcastMessage(self, message):
		print('Broadcast')
		print(str(self.factory.users))
		#  For each name and protocol item in the user dictionary 
		for name, protocol in self.factory.users.iteritems():
			#  Check to see if it is this instance, if not then pass the message to the client
			if protocol != self:
				protocol.sendLine(message)


###  ChatFactory class (inherits from Factory), used to create, store and manage the multiple connections to the server		

class ChatFactory(Factory):
	
	##  Constructor method, creates the user dictionary and then builds a TCP object factory, location of shared state variables.
	def __init__(self):
		self.users={}
		print('***** Welcome to the "An Seo" Server *****')
		print('*****    Server is listening....     *****')
	
	##  Returns a ChatProtocol object for each instance. Built in Factory method
	def buildProtocol(self, addr):
		'''This function returns an instance of ChatProtocol for each client received
		'''
		return ChatProtocol(self)

#  Create a Factory Instance  
cf = ChatFactory()
#  Tell the reactor to listen for incoming TCP streams on the default port, applying the rules set out in the Chat Protocol when it receives something,
#   via Chat Factory object
reactor.listenTCP(60001, cf)
#  Initiate the reactor
reactor.run()

		
		
		
		
		
		
		
