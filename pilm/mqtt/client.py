import paho.mqtt.client as mqtt
from loguru import logger
from ..config import Config


class Client(Config):
    def __init__(self, name = 'Client'):
        Config.__init__(self)
        self.name = name
        server = self.config.get('mqtt', 'server')
        port = int(self.config.get('mqtt', 'port'))
        self.client = self.get_client(server, port)

    def get_client(self, server, port):
        client = mqtt.Client()

        msg = (
          'Trying to connect to server {server}:{port}'
        )

        logger.debug(msg.format(server=server, port=port))

        client.connect(server, port)

        msg = (
          '{name} connected at {server}:{port}'
        )

        logger.info(msg.format(name=self.name, server=server, port=port))

        return client
