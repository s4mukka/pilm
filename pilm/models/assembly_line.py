import time
from loguru import logger

class AssemblyLine():
  def __init__(self, parent, id):
    self.id = id
    self.state = 'idle'
    self.parent = parent

  def change_to_idle(self):
    self.state = 'idle'

  def change_to_bulk(self):
    self.state = 'bulk'

  def produce_product(self, product_version, product_requirements):
    self.change_to_bulk()
    try:
      self.parent.stock.consume_stock(product_requirements)
      self.parent.send_to_deposit(self, product_version, product_requirements)
      time.sleep(10)
    except BufferError as err:
      logger.error(err)
    self.change_to_idle()
