import SocketServer
import select, socket

from replycodes import *
from channel import Channel

from rfchandler import RFCHandler

class Client(SocketServer.BaseRequestHandler):
	def __init__(self, request, client_address, server):
		

		self.squeue = []

		self.nick = ""
		self.user = ""
		self.realname = ""
		self.mode = ""
		self.channels = {}
		
		self.handlers = []
		
		SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)


	def setup(self):
		self.handlers.append(RFCHandler(self))

	def ident(self):
		"""
		Return the client identifier as included in many command replies.
		"""
		return '%s!%s@%s' % (self.nick, self.user, self.server.servername)

	def send_motd(self):
		self.send(':%s %s %s :End of MOTD command.' % (self.server.servername, RPL_ENDOFMOTD, self.nick))

	def send(self, message):
		print "<< " + message
		self.squeue.append(message + '\r\n')

	def handle(self):
		while True:
			ready_to_read, ready_to_write, in_error = select.select([self.request], [], [], 0.1)

			while self.squeue:
				self.request.send(self.squeue.pop(0))

			if not ready_to_read:
				continue

			data = self.request.recv(1024)
			
			if not data or len(data) == 0:
				break

			line = data.split("\n", 1)[0].rstrip()
			print ">> " + line

			if  ' ' in line:
				command, params = line.split(' ', 1)
			else:
				command, params = (line, '')

			try:
				for handler in self.handlers:
					hndlr = getattr(handler, 'on_%s' % (command.lower()), None)

					if not hndlr:
						print "unimplemented <%s %s>" % (command, params)
						continue

					print "<%s %s>" % (command, params)
					response = hndlr(params)
					
					if response:
						self.send(response)
			except Exception as e:
				print e
			
		self.request.close()