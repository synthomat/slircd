from replycodes import *
from channel import Channel


class Handler:
	def __init__(self, client):
		self.client = client
		self.server = client.server
		self.channels = client.channels

	def on_invite(self, params): pass
	def on_join(self, params): pass
	def on_kick(self, params): pass
	def on_name(self, params): pass
	def on_nick(self, params): pass
	def on_part(self, params): pass
	def on_privmsg(self, params): pass
	def on_topic(self, params): pass