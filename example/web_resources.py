import datetime
import xml
import re
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET


class TimeResource(Resource):
    def __init__(self, agent):
        self._agent = agent
        self._template = '<html><head><title>Current Time - Twisted Examples</title></head><body><h1>{0}</h1><p>{1}</p></body></html>'

    def render_GET(self, request):
        def parseResponse(response):
            finished = Deferred()
            response.deliverBody(TimeParser(finished))
            return finished

        def printTime(time, request):
            request.write(self._template.format(
                datetime.datetime.fromtimestamp(time),
                'This is the time from http://time.gov/widget/dhtml/actualtime.cgi'
            ))
            request.finish()

        def printError(failure, request):
            request.write(self._template.format('Error', failure.value))
            request.finish()

        d = self._agent.request('GET', 'http://time.gov/widget/dhtml/actualtime.cgi')
        d.addCallback(parseResponse)
        d.addCallback(printTime, request)
        d.addErrback(printError, request)
        return NOT_DONE_YET


class TimeParser(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10
        self.data = ""

    def dataReceived(self, bytes):
        if self.remaining:
            chunk = bytes[:self.remaining]
            self.remaining -= len(chunk)
            self.data += chunk

    def connectionLost(self, reason):
        result = re.search('time="(\d+)"', self.data)
        self.finished.callback(float(result.group(1)) / 1e6)
