import json
from loguru import logger

class Stock:
  def __init__(self, parent, items_type=[], refuel_topic=None):
    self.parent = parent
    self.items = self.start_stock(items_type)
    self.refuel_topic = refuel_topic

  def start_stock(self, items_type):
    return {
      item_type: {
        'quantity': 50,
        'level': self.set_level(50)
      } for item_type in items_type
    }

  def see_stock(self, item):
    logger.warning(self.items)
    return self.items[item]
  
  def has_stock(self, items):
    for item, value in items.items():
      if item not in self.items:
        if self.refuel_topic:
          data = {
            "factory": self.parent.name,
            "parts": [item]
          }
          self.parent.client.publish(self.refuel_topic, json.dumps(data))
        return False
      if self.items[item]['quantity'] < value['quantity']:
        if self.refuel_topic:
          data = {
            "factory": self.parent.name,
            "parts": [item]
          }
          self.parent.client.publish(self.refuel_topic, json.dumps(data))
        return False
    return True

  def consume_stock(self, items):
    for item, value in items.items():
      self.items[item]['quantity'] -= value['quantity']
      self.items[item]['level'] = self.set_level(self.items[item]['quantity'])
      if self.refuel_topic and self.items[item]['level'] == 'red':
        data = {
          "factory": self.parent.name,
          "parts": [item]
        }
        self.parent.client.publish(self.refuel_topic, json.dumps(data))

  def add(self, item):
    key, value = item
    self.items[key] = value

  def set_level(self, quantity):
    if quantity <= 10:
      return 'red'
    elif quantity <= 35:
      return 'yellow'
    return 'green'