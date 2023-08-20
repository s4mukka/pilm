from pilm.mqtt.publisher import Publisher
from random import randint, choices
from loguru import logger
import time
import json

class Simulator(Publisher):
    def send_order(self):
        data = {
            "product_version": "Pv{}".format(randint(1, 5)),
            "parts": choices(range(100), k=randint(47, 99))
        }
        self.send_message('order/purchase', json.dumps(data))

if __name__ == '__main__':
  simulator = Simulator('Simulator')
  try:
    while True:
      simulator.send_order()
      time.sleep(randint(3, 5))
  except KeyboardInterrupt:
    logger.info("The user stopped the execution")
