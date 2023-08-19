from .mqtt.subscriber import Subscriber
from .stock import Stock
from loguru import logger
import json

class Factory(Subscriber):
  def __init__(self):
    super().__init__()
    topic = self.config.get('factory', 'topic')
    self.client.on_message = self.on_message
    self.stock = Stock()
    self.subscribe(topic)

  def on_message(self, client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    log = (
      '{name} Received {payload} from {topic} topic'
    )

    logger.debug(log.format(name=self.name, payload=payload, topic=msg.topic))

    product_id, parts = payload.values()

    product_requirements = self.get_product_requirements(product_id, parts)

    if not self.stock.has_stock(product_requirements):
      log = (
        '{name} Out of stock to produce product {product_id}'
      )
      logger.debug(log.format(name=self.name, product_id=product_id))
      return

    self.produce_product(product_id, product_requirements)

  def produce_product(self, product_id, product_requirements):
    self.stock.consume_stock(product_requirements)
    self.send_to_deposit(product_id, product_requirements)

  def send_to_deposit(self, product_id, product_requirements):
    topic = self.config.get('deposit', 'topic')
    self.client.publish(
      topic,
      json.dumps(
        {
          "product_id": product_id,
          "requirements": product_requirements
        }
      )
    )
    log = (
      '{name} Produced the product {product_id}'
    )
    logger.debug(log.format(name=self.name, product_id=product_id))

  def get_product_requirements(self, product_id, parts):
    product_requirements = {}

    for part in parts:
      if part in product_requirements:
        product_requirements[part] += 1
      else:
        product_requirements[part] = 1

    log = (
      '{name} Product {product_id} requires {product_requirements}'
    )
    logger.debug(
      log.format(
        name=self.name,
        product_id=product_id,
        product_requirements=product_requirements
      )
    )

    return product_requirements
