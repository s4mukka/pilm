from .mqtt.subscriber import Subscriber
from .stock import Stock
from loguru import logger
import json
from .models.product import Product

class Deposit(Subscriber):
  def __init__(self):
    super().__init__()
    topic = self.config.get('deposit', 'topic')
    self.notification_topic = self.config.get('deposit', 'notification_topic')
    self.client.on_message = self.on_message
    self.stock = Stock([])
    self.subscribe(topic)
    self.notify()

  def on_message(self, client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    log = (
      '{name} Received {payload} from {topic} topic'
    )

    logger.debug(log.format(name=self.name, payload=payload, topic=msg.topic))

    product_version, requirements = payload.values()

    product = Product(product_version, requirements)

    self.stock.add(product.get_tuple())
    self.notify()

  def notify(self):
    self.ws_client.publish(self.notification_topic, json.dumps(self.stock.items))
    log = (
      '{name} notified {topic} topic'
    )
    logger.debug(log.format(name=self.name, topic=self.notification_topic))
