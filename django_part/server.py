from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import redis
import asyncio
import time
import asyncio_redis
import logging
import hashlib
from tasks import create_zip


logging.basicConfig(format=u'%(filename) 8s [LINE:%(lineno)d]# %(levelname)-3s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=u'log_server.log')


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        logging.info('Client successes connected.')

    def onOpen(self):
        print("WebSocket connection open.")
        logging.info('WebSocket connection open.')

    def onMessage(self, payload, isBinary):
        """
        It provides connectivity to radis-server and sending to client status of spiders for word-query.
        (which was got from client-part)

        :param:
            payload: data from part-client of autobahn;
            isBinary: data-binary from part-client of autobahn;
        """

        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            # print("Text message received: {0}".format(payload.decode('utf8')))
            print("Text message received: {0}".format(hashlib.sha224(payload).hexdigest()))

            payload = payload.decode('utf8').split(',')
            if payload[0] == 'query':
                try:
                    connection = yield from asyncio_redis.Connection.create(host='127.0.0.1', port=6379)
                    subscriber = yield from connection.start_subscribe()
                    query = hashlib.sha224(payload[1].encode('utf8')).hexdigest()
                    yield from subscriber.subscribe([query])

                    spiders_done = list()
                    while True:
                        reply = yield from subscriber.next_published()
                        print(reply.value)
                        if reply.value.startswith(query):
                            spiders_done.append(reply.value)
                            self.sendMessage(('query,' + payload[1] + ',' + reply.value).encode('utf-8'))
                        if len(spiders_done) > 2:
                            break

                    logging.info(u'Successes query to Redis: %s' % payload)
                except:
                    logging.error(u"Could'not connect to Redis.")
            elif payload[0] == 'zip':
                logging.info(u'Create zip: %s' % payload[1:])
                payload[1] = hashlib.sha224(payload[1].encode('utf8')).hexdigest()
                make = create_zip.delay(payload[1], payload[2:])
                while True:
                    if make.ready():
                        break
                logging.info('Created zip file')
                self.sendMessage((','.join(payload[:2])).encode('utf-8'))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        import trollius as asyncio

    try:
        factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
        factory.protocol = MyServerProtocol
        logging.info(u'Autobahn successfully connected to port.')
    except:
        logging.critical(u"Autobahn didn't connected to port.")

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)


    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
        logging.info(u'Successfully disconnected to port.')
