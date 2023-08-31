from .mqtt.subscriber import Subscriber
from .stock import Stock
from loguru import logger
from .models.assembly_line import AssemblyLine
import threading  
import json

class Factory(Subscriber):
  def __init__(self):
    super().__init__()
    self.topic = self.config.get('factory', 'topic')
    self.refuel_topic = 'refuel/{factory}'.format(factory=self.name)
    self.client.on_message = self.on_message
    self.notification_topic = self.config.get('factory', 'notification_topic')
    self.assembly_lines = [
      AssemblyLine(self, i) for i in range(
        int(self.config.get('factory', 'assembly_lines'))
      )
    ]
    self.stock = Stock(self, range(100), 'order/refuel')
    self.subscribe(self.topic, self.refuel_topic)

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

  def parse_refuel_topic(self, payload):
    for key, value in payload.items():
      item = self.stock.see_stock(int(key))
      item['quantity'] += value['quantity']
      self.stock.add(item)
    self.notify()

  def parse_topic(self, payload):
    product_version, parts = payload.values()

    product_requirements = self.get_product_requirements(product_version, parts)

    if not self.stock.has_stock(product_requirements):
      log = (
        '{name} Out of stock to produce product {product_version}'
      )
      logger.debug(log.format(name=self.name, product_version=product_version))
      return

    for assembly_line in self.assembly_lines:
      if assembly_line.state == 'idle':
        thread = threading.Thread(
          target=assembly_line.produce_product,
          args=(
            product_version,
            product_requirements,
          )
        )
        thread.start()
    self.notify()

  def send_to_deposit(
      self, assembly_line: AssemblyLine, product_version, product_requirements
  ):
    topic = self.config.get('deposit', 'topic')
    self.client.publish(
      topic,
      json.dumps(
        {
          "product_version": product_version,
          "requirements": product_requirements
        }
      )
    )
    log = (
      '{name} Produced the product {product_version} using assembly line {assembly_line_id}'
    )
    logger.debug(
      log.format(
        name=self.name,
        product_version=product_version,
        assembly_line_id=assembly_line.id
      )
    )

  def notify(self):
    data = self.stock.items
    self.ws_client.publish(self.notification_topic, json.dumps(data))
    log = (
      '{name} notified {topic} topic'
    )
    logger.debug(log.format(name=self.name, topic=self.notification_topic))

  def get_product_requirements(self, product_version, parts):
    product_requirements = {}

    for part in parts:
      if part in product_requirements:
        product_requirements[part]['quantity'] += 1
      else:
        product_requirements[part] = {"quantity": 1}

    log = (
      '{name} Product {product_version} requires {product_requirements}'
    )
    logger.debug(
      log.format(
        name=self.name,
        product_version=product_version,
        product_requirements=product_requirements
      )
    )

    return product_requirements
