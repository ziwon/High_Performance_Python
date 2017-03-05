#asyncio_echo_client_protocol.py


import asyncio
import functools
import logging
import sys

MESSAGES = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()

class EchoClient(asyncio.Protocol):
    # the class constructor accepts two args
    #  - a list of the messages to send
    #  - a Future instance to use to signal that the client has completed a
    #  cycle of work by receiving a response from the server
    def __init__(self, messages, future):
        super().__init__()
        self.messages = messages
        self.log = logging.getLogger('EchoClient')
        self.f = future

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug(
            'connecting to {} port {}'.format(*self.address)
        )
        # This could be transport.writelines() except that
        # would make it harder to show each part of the message
        # being sent.
        for msg in self.messages:
            transport.write(msg)
            self.log.debug('sending {!r}'.format(msg))
        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))

    # when either an end-of-file marker is received or the connection is closed
    # from the server's side, the local transport object is closed and the
    # future object is marked as done by sending a result
    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)

    def connection_lost(self, exc):
        self.log.debug('server closed connection')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)
        super().connection_lost(exc)

# Normally the protocol class is passed to the event loop to create the
# connection. In this case, the event loop has no facility for passing extra
# arguments to the protocol constructor, it is necessary to create a partial to
# wrap the client class and pass the list of messages to send and the Future
# instance.
client_completed = asyncio.Future()

client_factory = functools.partial(
    EchoClient,
    messages=MESSAGES,
    future=client_completed,
)

factory_coroutine = event_loop.create_connection(
    client_factory,
    *SERVER_ADDRESS,
)

log.debug('waiting for client to complete')
try:
    event_loop.run_until_complete(factory_coroutine)
    event_loop.run_until_complete(client_completed)
finally:
    log.debug('closing event loop')
    event_loop.close()