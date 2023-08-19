import paho.mqtt.client as mqtt
from loguru import logger
from ..config import Config
import sys

class Client(Config):
    def __init__(self, name = None):
        super().__init__()
        if name == None:
            name = self.config.get('pilm', 'role')
        self.name = name.upper()
        server = self.config.get('mqtt', 'server')
        port = int(self.config.get('mqtt', 'port'))
        self.client = self.get_client(server, port)

    def get_client(self, server, port):
        client = mqtt.Client()

        msg = (
          '{name} Trying to connect to server {server}:{port}'
        )

        logger.debug(msg.format(name=self.name, server=server, port=port))

        try:
          client.connect(server, port)

          msg = (
            '{name} connected at {server}:{port}'
          )
          logger.info(msg.format(name=self.name, server=server, port=port))

          return client
        except OSError:
          msg = (
            '{name} cannot connect to server {server}:{port}'
          )
          logger.error(msg.format(name=self.name, server=server, port=port))
          sys.exit(0)


