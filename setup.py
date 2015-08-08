try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='twisted-example-web-chat',
    version='0.0.1',
    author='Adam Englander',
    author_email='adamenglander@yahoo.com',
    url='http://adamknowsstuff.com/',
    summary='Twisted Web Server Example - Chat Server',
    license='MIT',
    description='An example of how to host a website that is a chat application with web sockets',
    install_requires=['autobahn', 'twisted'],
    data_files=[]
)
