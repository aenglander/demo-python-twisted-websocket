from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from twisted.internet.defer import log


class ServerFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(ServerFactory, self).__init__(*args, **kwargs)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            log.debug("registered client {peer}", peer=client.peer)
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            log.debug("unregistered client {client}", client=client)
            self.clients.remove(client)

    def broadcast(self, msg):
        log.debug("broadcasting prepared message '{msg}' ..", msg=msg)
        message = self.prepareMessage(msg.encode('utf8'))
        for c in self.clients:
            c.sendPreparedMessage(message)
            log.debug("prepared message sent to {peer}", peer=c.peer)


class ServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        log.debug("Client connecting: {peer}", peer=request.peer)
        self.factory.register(self)

    def onOpen(self):
        log.debug("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            log.debug("Binary message received: {bytes} bytes", bytes=len(payload))
        else:
            message_string = "{1} ({0})".format(self.peer, payload).decode('utf8')
            log.debug("Text message received: {message}", message=message_string)
            self.factory.broadcast(message_string)

    def onClose(self, wasClean, code, reason):
        self.factory.unregister(self)
        log.debug("WebSocket connection closed: {reason}", reason=reason)
