from .mqtt.subscriber import Subscriber
from .stock import Stock
from loguru import logger
import json

class Provider(Subscriber):
  def __init__(self):
    super().__init__()
    topic = self.config.get('provider', 'topic')
    self.notification_topic = self.config.get('provider', 'notification_topic')
    self.client.on_message = self.on_message
    self.subscribe(topic)
    self.notify()

  def on_message(self, client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    log = (
      '{name} Received {payload} from {topic} topic'
    )

    logger.debug(log.format(name=self.name, payload=payload, topic=msg.topic))

    warehouse, parts = payload.values()

    self.send_parts_required(warehouse, parts)

  def send_parts_required(self, warehouse, parts):
    parts_required = self.get_parts_required(warehouse, parts)

    topic = 'refuel/{warehouse}'.format(warehouse=warehouse)
    self.client.publish(topic, json.dumps(parts_required))
    log = (
      '{name} send refuel to {topic} topic'
    )
    logger.debug(log.format(name=self.name, topic=topic))

  def get_parts_required(self, factory, parts):
    parts_required = {}

    for part in parts:
      parts_required[part] = {"quantity": 10}

    log = (
      '{name} Fectory {factory} requires {parts_required}'
    )
    logger.debug(
      log.format(
        name=self.name,
        factory=factory,
        parts_required=parts_required
      )
    )

    return parts_required
