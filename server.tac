from twisted.application import service

# this is the core part of any tac file, the creation of the root-level
# application object
from example.service import Service

application = service.Application("Demo application")

service = Service(8080)
service.setServiceParent(application)
