from .mqtt.subscriber import Subscriber
from .stock import Stock
from loguru import logger
import json

class Factory(Subscriber, Stock):
  def __init__(self):
    super().__init__()
    topic = self.config.get('factory', 'topic')
    self.client.on_message = self.on_message
    self.subscribe(topic)

  def on_message(self, client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    log = (
      '{name} Received {payload} from {topic} topic'
    )

    logger.debug(log.format(name=self.name, payload=payload, topic=msg.topic))

    product_id, parts = payload.values()

    product_require = {}

    for part in parts:
      if part in product_require:
        product_require[part] += 1
      else:
        product_require[part] = 1

    log = (
      'Product {product_id} requires {product_require}'
    )
    logger.debug(
      log.format(
        name=self.name,
        product_id=product_id,
        product_require=product_require
      )
    )
