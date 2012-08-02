class Channel:
	def __init__(self, name):
		self.topic = ""
		self.topic_by = ""
		self.clients = {}
		self.name = name

		self.modes = {
			"o": [],	# give/take channel operator privileges
			"b": [],	# set a ban mask to keep users out
			"v": [],	# give/take the ability to speak on a moderated channel
			"p": False, # private channel flag
			"s": False, # secret channel flag
			"i": False, # invite-only channel flag
			"t": False, # topic settable by channel operator only flag
			"n": False, # no messages to channel from clients on the outside
			"m": False, # moderated channel
			"l": False, # set the user limit to channel
			"k": False  # set a channel key (password)
		}

	def join(self, client):
		self.clients[client.nick] = client
		client.channels[self.name] = self

		client.send(':%s TOPIC %s :%s' % (self.topic_by, self.name, self.topic))

		for c in self.clients:	
			self.clients[c].send(':%s JOIN :%s' % (client.nick, self.name))
	
		nicks = [self.clients[c].nick for c in self.clients]

		client.send(':%s 353 %s = %s :%s' % (client.server.servername, client.nick, self.name, ' '.join(nicks)))
		client.send(':%s 366 %s %s :End of /NAMES list' % (client.server.servername, client.nick, self.name))


	def privmsg(self, client, text):
		for nick in self.clients:
			if self.clients[nick] == client:
				continue

			self.clients[nick].send(':%s PRIVMSG %s :%s' % (client.ident(), self.name, text.lstrip(':')))

	def mode(self, client, modes):
		for c in self.clients:	
			self.clients[c].send(':%s MODE %s %s %s' % (client.server.servername, self.name, modes, client.nick))
