from .client import Client
from loguru import logger

class Subscriber(Client):
  def subscribe(self, topic):
    self.client.subscribe(topic)
    msg = (
      '{name} subscribed to topic {topic}'
    )
    logger.debug(msg.format(name=self.name, topic=topic))
    self.client.loop_forever()

  def on_message(self, client, userdata, msg):
    pass
