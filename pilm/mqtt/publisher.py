from .client import Client
from loguru import logger

class Publisher(Client):
    def send_message(self, topic, message):
        self.client.publish(topic, message)
        msg = (
            '{name} sent {message} to {topic}'
        )
        logger.debug(msg.format(name=self.name, message=message, topic=topic))
