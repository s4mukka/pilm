from .mqtt.subscriber import Subscriber
from .stock import Stock
from loguru import logger
import json

class Warehouse(Subscriber):
  def __init__(self):
    super().__init__()
    self.topic = self.config.get('warehouse', 'topic')
    self.refuel_topic = 'refuel/{warehouse}'.format(warehouse=self.name)
    self.notification_topic = self.config.get('warehouse', 'notification_topic')
    self.client.on_message = self.on_message
    self.stock = Stock(self, range(100), 'provider/refuel')
    self.subscribe(self.topic, self.refuel_topic)
    self.notify()

  def on_message(self, client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    log = (
      '{name} Received {payload} from {topic} topic'
    )

    logger.debug(log.format(name=self.name, payload=payload, topic=msg.topic))

    if msg.topic == self.topic:
      self.parse_topic(payload)
    elif msg.topic == self.refuel_topic:
      self.parse_refuel_topic(payload)

  def parse_topic(self, payload):
    factory, parts = payload.values()
    self.send_parts_required(factory, parts)

  def parse_refuel_topic(self, payload):
    for key, value in payload.items():
      item = self.stock.see_stock(int(key))
      item['quantity'] += value['quantity']
      self.stock.add(item)
    self.notify()

  def send_parts_required(self, factory, parts):
    parts_required = self.get_parts_required(factory, parts)

    if not self.stock.has_stock(parts_required):
      log = (
        '{name} Out of stock to refuel parts {parts_required}'
      )
      logger.debug(log.format(name=self.name, parts_required=parts_required))
      return
    self.stock.consume_stock(parts_required)
    topic = 'refuel/{factory}'.format(factory=factory)
    self.client.publish(topic, json.dumps(parts_required))
    log = (
      '{name} send refuel to {topic} topic'
    )
    logger.debug(log.format(name=self.name, topic=topic))
    self.notify()

  def notify(self):
    self.ws_client.publish(self.notification_topic, json.dumps(self.stock.items))
    log = (
      '{name} notified {topic} topic'
    )
    logger.debug(log.format(name=self.name, topic=self.notification_topic))

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
