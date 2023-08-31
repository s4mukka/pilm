from pilm.mqtt.publisher import Publisher
from random import randint, choice
from loguru import logger
import time
import json

products = [
  {
    "product_version": "Pv1",
    "parts": list(range(48)) + list(range(48, 60))
  },
  {
    "product_version": "Pv2",
    "parts": list(range(48)) + list(range(60, 70))
  },
  {
    "product_version": "Pv3",
    "parts": list(range(48)) + list(range(70, 80))
  },
  {
    "product_version": "Pv4",
    "parts": list(range(48)) + list(range(80, 90))
  },
  {
    "product_version": "Pv5",
    "parts": list(range(48)) + list(range(90, 100))
  },
]

class Simulator(Publisher):
    def send_order(self):
        data = choice(products)
        self.send_message('order/purchase', json.dumps(data))

if __name__ == '__main__':
  simulator = Simulator('Simulator')
  try:
    while True:
      simulator.send_order()
      time.sleep(randint(3, 5))
  except KeyboardInterrupt:
    logger.info("The user stopped the execution")
