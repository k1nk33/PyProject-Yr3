#!/usr/bin/jython
from javax.swing import SwingConstants, ScrollPaneConstants, JFrame ,JPanel, JLabel, JButton, JTextPane, JTextArea, JTextField , JOptionPane, BorderFactory , GroupLayout , JScrollPane, KeyStroke
from java.awt import Dimension, Color, Font, AWTKeyStroke
from java.awt.event import KeyEvent, KeyAdapter
from javax.swing.text import SimpleAttributeSet
from threading import Thread
import telnetlib

###  ChatApp class to build the login GUI and set up the connection (inherits from JFrame)

class ChatApp(JFrame):
	
	##  Constructor function, initiate the base classes and call the GUI
	
	def __init__(self):
		'''Calls the base class and main UI
		'''
		#  Call to the super class, initiates associated base classes
		super(ChatApp, self).__init__()
		#  Call the Initial UI
		self.initUI()
	
	##  Build the GUI for login, uses GroupLayout Manager for component positioning
		
	def initUI(self):
		'''Initial UI and Widget creation takes place here!
		'''
		self.setContentPane = JPanel()
		#self.setDefaultLookAndFeelDecorated(True)
		#  Borders
		foreground_colour = Color(30,57,68)
		background_colour = Color(247,246,242)
		window_background = Color(145,190,210)
		self.border = BorderFactory.createLoweredBevelBorder()
		self.border2 = BorderFactory.createLineBorder(foreground_colour, 1, True)
		#  Fonts
		self.entry_font= Font("Ubuntu Light",  Font.BOLD, 20)
		self.label_font= Font("Ubuntu Light",  Font.BOLD, 17)
		self.btn_font=Font("Ubuntu Light", Font.BOLD, 15)
		#  Layout start
		layout=GroupLayout(self.getContentPane())
		self.getContentPane().setLayout(layout)	
		layout.setAutoCreateGaps(True)
		layout.setAutoCreateContainerGaps(True)
		self.setPreferredSize(Dimension(300, 150))
		#  Create the labels
		user_label= JLabel(" Username : ",JLabel.LEFT, font=self.label_font) 
		server_label=JLabel("  Server  : ", JLabel.LEFT, font=self.label_font)
				
		#  Colours
		user_label.setForeground(foreground_colour)
		server_label.setForeground(foreground_colour)
		
		#  Create the text entries
		self.username=JTextField(actionPerformed=self.continueEvent, border=self.border2,  font = self.entry_font)
		self.server=JTextField(actionPerformed=self.continueEvent, border=self.border2,  font = self.entry_font)
		
		#  Colours
		self.username.setBackground(background_colour)
		self.server.setBackground(background_colour)
		self.username.setForeground(foreground_colour)
		self.server.setForeground(foreground_colour)
		
		#  Allow editable
		self.username.setEditable(True)
		self.server.setEditable(True)
		
		#  Create the buttons
		quit_btn=JButton("  Quit!  ", actionPerformed=self.closeEvent, border=self.border2, font=self.btn_font)
		go_btn=JButton("   Go!   ", actionPerformed=self.continueEvent, border=self.border2, font=self.btn_font)
		#  Colours
		quit_btn.setBackground(background_colour)
		go_btn.setBackground(background_colour)
		quit_btn.setForeground(foreground_colour)
		go_btn.setForeground(foreground_colour)
		
		#  Setting up the horizontal groups parameters
		layout.setHorizontalGroup(layout.createSequentialGroup()
		
			#  Left side
			.addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING)
				.addComponent(user_label)
				.addComponent(server_label))
				
			#  Right side
			.addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
				.addComponent(self.username)
				.addComponent(self.server)
				.addGroup(layout.createSequentialGroup()
					.addComponent(quit_btn)
					.addComponent(go_btn)))
		)
		
		#  Setting up Vertical Groups
		layout.setVerticalGroup(layout.createSequentialGroup()
			#  Top group
			.addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
				.addComponent(user_label)
				.addComponent(self.username))
			#  Middle group
			.addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
				.addComponent(server_label)
				.addComponent(self.server))
			#  Bottom group
			.addGroup(layout.createParallelGroup()
				.addComponent(quit_btn)
				.addComponent(go_btn))
		)
		
		#  Finalise the GUI	
		layout.linkSize(SwingConstants.HORIZONTAL, [quit_btn,go_btn])
		self.getContentPane().setBackground(window_background)
		self.pack()
		self.setTitle('Chat Login')
		self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
		self.setLocationRelativeTo(None)
		self.setVisible(True)
		
	##  Event driven funtion to respond to quit button click
	
	def closeEvent(self,event):	
		'''Function to close the login window
		'''
		print("Goodbye!")
		exit()		
	
	
	##  Event driven function to respond to send button click, grabs text and sends it down the wire	
	
	def continueEvent(self,event):
		'''Function that retreives the login details for sending to the server
		'''	
		#  Grab the text that has been entered
		user = self.username.getText()
		Host = self.server.getText()
		#  Default port
		Port=60001
		connected=False
		while not connected:
		#  Try make a connection except when there isn't one available, then quit program'
			try:
				tn=telnetlib.Telnet(Host, Port)
				connected=True
				continue
			except:
				JOptionPane.showMessageDialog(self,'Connection Error, No Server Available!')
				self.username.setText('')
				self.server.setText('')
				self.username.requestFocusInWindow()
				return
		#  Listen for a response	
		response = tn.read_until('<<<')
		print(response)
		#  Acknowledge with the username
		tn.write(user+'\r\n')
		#  Receive validation of name, present dialog if not valid
		valid_name = tn.read_until('<')
		valid_name.strip()
		v_name, delim = valid_name.split('<')
		if v_name.strip() != 'OK':
			JOptionPane.showMessageDialog(self,'Bad Username, please choose another')
			self.username.setText('')
			self.username.requestFocusInWindow()
			return
		#  Set the login GUI to hidden
		self.setVisible(False)  ##   <<<<<<  I have no idea why this doesn't work but I suspect it's something to do with either inheritance or having 2 class instances
		#  Call the main program, pass the connection as a parameter
		ChatClient(user,response , tn)

###  Main ChatClient class, inherits from JFrame

class ChatClient(JFrame):
	
	##  Constructor method, receives the variables from the ChatApp class as parameters
	
	def __init__(self, name, greeting, tn):
		'''Constructor, initialises base class & assigns variables
		'''
		# Call to the super method to take care of the base class(es)
		super(ChatClient, self).__init__()
		#  Assign the relevent variable names
		self.username=name
		self.greeting=greeting
		self.tn = tn
		self.no_users=[]
		#  Initiate the Threaded function for receiving messages
		t1=Thread(target=self.recvFunction)
		#  Set to daemon 
		t1.daemon=True
		t1.start()
		#Call the main UI
		uI=self.clientUI()
		
	##  Main GUI building function
	
	def clientUI(self):
		'''ClientUI and Widget creation
		'''
		#  Colours
		foreground_colour = Color(30,57,68)
		background_colour = Color(247,246,242)
		window_background = Color(145,190,210)
		#  Borders
		self.border2=BorderFactory.createLineBorder(foreground_colour,1, True)
		#  Fonts
		self.font= Font("Ubuntu Light",  Font.BOLD, 20)
		self.label_font= Font("Ubuntu Light",  Font.BOLD, 17)
		self.label_2_font= Font( "Ubuntu Light",Font.BOLD, 12)
		self.btn_font=Font("Ubuntu Light", Font.BOLD, 15)
		
		#  Set the layout parameters
		self.client_layout=GroupLayout(self.getContentPane())
		self.getContentPane().setLayout(self.client_layout)	
		self.getContentPane().setBackground(window_background)
		self.client_layout.setAutoCreateGaps(True)
		self.client_layout.setAutoCreateContainerGaps(True)
		self.setPreferredSize(Dimension(400, 450))
		
		#  Create widgets and assemble the GUI
		#  Main display area
		self.main_content=JTextPane()
		self.main_content.setBackground(background_colour)
		#self.main_content.setForeground(foreground_colour)
		self.main_content.setEditable(False)
		#  Message entry area  		
		self.message=JTextArea( 2,2, border=self.border2, font=self.label_font, keyPressed=self.returnKeyPress)
		self.message.requestFocusInWindow()	
		self.message.setBackground(background_colour)
		self.message.setForeground(foreground_colour)
		self.message.setLineWrap(True)
		self.message.setWrapStyleWord(True)
		self.message.setBorder(BorderFactory.createEmptyBorder(3,3,3,3))
		self.message.getInputMap().put(KeyStroke.getKeyStroke(KeyEvent.VK_ENTER,0), self.returnKeyPress) 
		#  BUttons
		quit_btn=JButton("Quit!", actionPerformed=ChatApp().closeEvent, border=self.border2, font=self.btn_font)
		go_btn=JButton("Send", actionPerformed=self.grabText, border=self.border2, font=self.btn_font)
		quit_btn.setBackground(background_colour)
		go_btn.setBackground(background_colour)
		quit_btn.setForeground(foreground_colour)
		go_btn.setForeground(foreground_colour)
		
		# Make scrollable
		self.scroll_content=JScrollPane(self.main_content)
		self.scroll_content.setPreferredSize(Dimension(150,275))
		self.scroll_content.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER)
		self.scroll_content.setViewportView(self.main_content)
		self.scroll_content.setBackground(Color.WHITE)
		self.scroll_message=JScrollPane(self.message)
		self.scroll_message.setPreferredSize(Dimension(150,20))
		self.scroll_message.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS)
		
		# Test user label, still not updating after first round of messages
		self.user_label=JLabel(" Users online : %s "%(str(len(self.no_users))),JLabel.RIGHT, font=self.label_2_font)
		
		#  Assemble the components
		#  Horizontal layout
		self.client_layout.setHorizontalGroup(self.client_layout.createParallelGroup()
				.addComponent(self.scroll_content)
				.addGroup(self.client_layout.createParallelGroup(GroupLayout.Alignment.CENTER)
					.addComponent(self.scroll_message))
				.addGroup(self.client_layout.createSequentialGroup()
					.addComponent(quit_btn)
					.addComponent(go_btn).addGap(20))
				.addGroup(self.client_layout.createParallelGroup()
					.addComponent(self.user_label))
		)
		
		#  Vertical layout
		self.client_layout.setVerticalGroup(self.client_layout.createSequentialGroup()
			.addGroup(self.client_layout.createParallelGroup()
				.addComponent(self.scroll_content))
				.addComponent(self.scroll_message)
				.addGroup(self.client_layout.createParallelGroup()
					.addComponent(quit_btn)
					.addComponent(go_btn))
				.addGroup(self.client_layout.createParallelGroup()
					.addComponent(self.user_label))
		)
		
		#  Finalise the GUI
		self.client_layout.linkSize(SwingConstants.HORIZONTAL, [quit_btn,go_btn, self.user_label])
		self.pack()
		self.message.requestFocusInWindow()
		self.setTitle(">>>   Client %s   <<<"%self.username)
		self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
		self.setLocationRelativeTo(None)
		self.setVisible(True)
		#  Display the server greeting
		self.appendText('\n'+self.greeting+'\n')
	
			
	##  Function responsible for receiving and processing new messages
	
	def recvFunction(self):
		'''A function to control the receiving of data from the connection
		'''
		#  While the connection is available
		while self.tn:
			#  Try to receive data using "<<<" as the delimiter
			try:
				message = self.tn.read_until('<<<')
				#  If a message is received
				if message:
					garb, message=message.split('>>>')
					message, garb = message.split('<<<')
					message = ('\n'+message+'\n')
					#  Call the append text function
					self.appendText(message)
			#  Except if there is no data available		
			except:
				#print('No message')	
				pass
	##  Event driven function to retrieve and send data to the server
	
	def grabText(self, event): 
		'''Function to repeatedly grab new messages entered into the text 
		area and display them in the main text area. Resets the entry area
		'''
		#  Grab the text from the text area
		text=self.message.getText()
		#  Don't allow an empty string through
		if text=='':
			return
		text=text.strip()
		#  Call the append text function
		self.appendText('\nYou : '+text+'\n', self.username)
		#  Reset the text to be empty and grab focus so that it is ready for new text input
		self.message.requestFocusInWindow()
		self.message.setText('')
		#  Send the message to the server
		data=text.encode()
		self.tn.write(data+'\r\n')

	##  Function to handle appending of messages
	
	def appendText(self, message, user=None):
		'''This function takes care of appending any new messages to the content area
		'''
		message_label=JTextArea(message,2,3, font=self.label_2_font)
		#  If this is a message from the grab text function, create a new label, assign it's colours
		if user!=None:
			message_label.setBackground(Color(240,240,240))
			message_label.setForeground(Color(129,129,129))
		#  Otherwise set the format for receive function (no user passed in)	
		else:
			message_label.setBackground(Color(215,215,215))
			message_label.setForeground(Color(40,153,153))
		
		#  Format and style options for the new message labels	
		message_label.setEditable(False)
		message_label.setLineWrap(True)
		message_label.setWrapStyleWord(True)
		message_label.setBorder(BorderFactory.createLineBorder( Color(247,246,242),4))
		#  Sets the positioning of messages
		self.main_content.setCaretPosition(self.main_content.getDocument().getLength())
		doc = self.main_content.getStyledDocument()
		attr=SimpleAttributeSet()
		self.main_content.insertComponent(message_label)
		# Essential for jtextarea to be able to stack message
		doc.insertString( self.main_content.getDocument().getLength(),'\n ', attr)
		# Not sure if needed
		self.main_content.repaint()
		
		###  This is a late edit so it isn't included in the documentation. Basically trying to dynamically update the number
		###  of users label at runtime. Works for incrementing the value but not decrementing it.
		
		print(message)
		#  Only split the message if there are enough values to split (greeting messages differ in format to chat messages)
		try:
			user, text=message.split(' : ')
		except:
			return
			
		#print('Split values are %s %s'%(user, text))
		user=str(user.strip())
		#print(self.no_users)
		#print(user+' : '+text)
		#  If the user already in the list, pass
		if user in self.no_users:
			if text == ('User %s amach sa teach !'%user):
				self.no_users.remove(user)
				print('User % removed'%user)
			
		else:
			#print('User %s not in list'%user)
			if str(user) == 'You':
				#print('User is equal to "You"')
				return 
			self.no_users.append(user)
			print('User appended')
			self.number_users=len(self.no_users)
			#print('Length of user list is '+str(self.number_users))
	
		self.user_label2=JLabel(" Users online : %s "%str(len(self.no_users)),JLabel.RIGHT, font=self.label_2_font)
		#print('Label created')
		#print('Attempt to replace label')
		self.client_layout.replace(self.user_label, self.user_label2) 
		self.user_label = self.user_label2
		self.user_label.repaint()
		self.user_label.revalidate()
		print('Label updated')
	
	##  Function to control return button press in message field

	def returnKeyPress(self,event):
		'''This function creates an object for return key press when inside the message entry area,
		creates an object of KeyAdapter and tests keycode for a match, responds with grab text callback		
		'''
		key_object=Key()
		key_value=key_object.keyPressed(event)
		if key_value == 10:
			self.grabText(event)

###  Class to collect key presses, inherits from KeyAdapter
			
class Key(KeyAdapter):	
	'''Inherits from KeyAdapter and provides the keyPressed function for the key press event,
	returns key for testing match
	'''	
	##  EVent driven function to grab key press
	
	def keyPressed(self, event):
		'''Key pressed function for key press event, grabs keycode and returns the value for testing
		'''
		key=event.getKeyCode()
		return key		

###  Start the program		
if __name__ == '__main__':
	ChatApp()		
