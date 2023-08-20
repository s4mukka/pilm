from .mqtt.subscriber import Subscriber
from .stock import Stock
from loguru import logger
import json

class Factory(Subscriber):
  def __init__(self):
    super().__init__()
    topic = self.config.get('factory', 'topic')
    self.client.on_message = self.on_message
    self.notification_topic = self.config.get('factory', 'notification_topic')
    self.stock = Stock(range(100))
    self.subscribe(topic)

  def on_message(self, client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    log = (
      '{name} Received {payload} from {topic} topic'
    )

    logger.debug(log.format(name=self.name, payload=payload, topic=msg.topic))

    product_version, parts = payload.values()

    product_requirements = self.get_product_requirements(product_version, parts)

    if not self.stock.has_stock(product_requirements):
      log = (
        '{name} Out of stock to produce product {product_version}'
      )
      logger.debug(log.format(name=self.name, product_version=product_version))
      return

    self.produce_product(product_version, product_requirements)

  def produce_product(self, product_version, product_requirements):
    self.stock.consume_stock(product_requirements)
    self.send_to_deposit(product_version, product_requirements)
    self.notify()

  def send_to_deposit(self, product_version, product_requirements):
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
      '{name} Produced the product {product_version}'
    )
    logger.debug(log.format(name=self.name, product_version=product_version))

  def notify(self):
    self.ws_client.publish(self.notification_topic, json.dumps(self.stock.items))
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
