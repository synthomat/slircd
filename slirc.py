#!/usr/bin/env python

import SocketServer
from irc.client import Client
import config


class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	daemon_threads = True
	allow_reuse_address = True

	def __init__(self, server_addr):
		self.servername = config.HOST
		self.channels = {} # Existing channels (IRCChannel instances) by channelname
		self.clients = {}  # Connected clients (IRCClient instances) by nickname
		SocketServer.TCPServer.__init__(self, server_addr, Client)

if __name__ == "__main__":
	server = Server((config.HOST, config.PORT))
	server.serve_forever()