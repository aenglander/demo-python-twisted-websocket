import os
from autobahn.twisted.resource import WebSocketResource
from twisted.application import service
from twisted.internet import reactor
from twisted.web import static, server
from twisted.web.client import Agent
from example.socket_server import ServerFactory, ServerProtocol
from example.web_resources import TimeResource


class Service(service.Service):
    def __init__(self, port):
        self.port = port
        self.server = None

    def startService(self):
        root = static.File(os.path.join(os.path.dirname(__file__), 'public'))

        factory = ServerFactory()
        factory.protocol = ServerProtocol
        factory.startFactory()
        socket = WebSocketResource(factory)
        root.putChild('socket', socket)

        time = TimeResource(Agent(reactor))
        root.putChild('time', time)

        site = server.Site(root)

        self.server = reactor.listenTCP(self.port, site)

    def stopService(self):
        return self.server.stopListening()
