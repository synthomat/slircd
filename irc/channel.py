from replycodes import *

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

    def clients_with_modes(self):
        clients = []

        for c in self.clients:
            if c in self.modes['o']:
                clients.append('@' + c)
            elif c in self.modes['v']:
                clients.append('+' + c)
            else:
                clients.append(c)

        return clients


    def join(self, client):
        self.clients[client.nick] = client
        client.channels[self.name] = self

        self.broadcast(':%s JOIN :%s' % (client.ident(), self.name))

        if len(self.clients) == 1:
            self.modes['o'].append(client.nick)

        nicks = self.clients_with_modes()


        client.send(RPL_NAMREPLY, ' '.join(nicks), '= ' + self.name)
        client.send(RPL_ENDOFNAMES, 'End of /NAMES list', self.name)


    def broadcast(self, msg):
        for c in self.clients:
            self.clients[c].sendraw(msg)

    def privmsg(self, client, text):
        for nick in self.clients:
            if self.clients[nick] == client:
                continue

            self.clients[nick].sendraw(':%s PRIVMSG %s :%s' % (client.ident(), self.name, text))

    def mode(self, client, modes, dst):
        for c in self.clients:
            self.clients[c].sendraw(':%s MODE %s %s %s' % (client.ident(), self.name, modes, dst))
