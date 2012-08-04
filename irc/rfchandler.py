from replycodes import *
from channel import Channel
from handler import Handler

class RFCHandler(Handler):
    def on_invite(self, params):
        return

    def on_join(self, params):
        channels = params.split(' ', 1)[0] # ignore keys

        for channel_name in channels.split(','):
            channel_name = channel_name.lstrip(':').strip(' ')

            channel = self.server.channels.setdefault(channel_name, Channel(channel_name))
            channel.join(self.client)

    def on_kick(self, params):
        return

    def on_mode(self, params):
        channel, modes, nick = params.split(' ')
        self.channels[channel].mode(self.client, modes, nick)

    def on_nick(self, params):
        nick = params

        if self.client.nick:
            return

        if nick in self.server.clients:
            return

        self.client.nick = nick
        self.client.send(RPL_WELCOME, SRV_WELCOME)
        self.client.send_motd()

        self.server.clients[nick] = self.client

    def on_part(self, params):
        return

    def on_privmsg(self, params):
        channel_name, message = params.split(' ', 1)

        if channel_name in self.channels:
            self.channels[channel_name].privmsg(self.client, message)

    def on_topic(self, params):
        return

    def on_user(self, params):
        user, mode, unused, realname = params.split(' ', 3)
        self.user = user
        self.mode = mode
        self.realname = realname