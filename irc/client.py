import SocketServer
import select, socket

from replycodes import *
from rfchandler import RFCHandler
import config

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
        return '%s!%s@%s' % (self.nick, self.user, self.server.servername)

    def send_motd(self):
        self.send(RPL_ENDOFMOTD, 'End of MOTD command.')

    def send(self, cmd, msg, chan=None, sender=None, delimiter=True):
        if not sender: sender = self.server.servername
        if delimiter: msg = ':' + msg

        if chan:
            chan = ' ' + chan
        else:
            chan = ''



        msg = ':%s %s %s%s %s' % (sender, cmd, self.nick, chan, msg)
        self.sendraw(msg)

    def sendraw(self, msg):
        print "<< (%s): %s "% (self.nick, msg)
        self.squeue.append(msg)

    def handle(self):
        while True:
            ready_to_read, ready_to_write, in_error = select.select([self.request], [], [], 0.1)

            while self.squeue:
                self.request.send(self.squeue.pop(0) + "\r\n")

            if not ready_to_read:
                continue

            data = self.request.recv(1024)

            if not data or len(data) == 0:
                break

            line = data.split("\n", 1)[0].rstrip()
            print ">> (%s): %s" % (self.nick, line)

            if  ' ' in line:
                command, params = line.split(' ', 1)
            else:
                command, params = (line, '')

            #try:
            for handler in self.handlers:
                hndlr = getattr(handler, 'on_%s' % (command.lower()), None)

                if not hndlr:
                    print "unimplemented <%s %s>" % (command, params)
                    continue

                response = hndlr(params)

                if response:
                    self.send(response)
            #except Exception as e:
            #    print e
			
        self.request.close()