class Stock:
  def __init__(self, items_type=[]):
    self.items = self.start_stock(items_type)

  def start_stock(self, items_type):
    return {
      item_type: {
        'quantity': 50,
        'level': self.set_level(50)
      } for item_type in items_type
    }

  def see_stock(self, item):
    return self.items[item]
  
  def has_stock(self, items):
    for item, value in items.items():
      if item not in self.items:
        return False
      if self.items[item]['quantity'] < value['quantity']:
        return False
    return True
  
  def consume_stock(self, items):
    for item, value in items.items():
      self.items[item]['quantity'] -= value['quantity']
      self.items[item]['level'] = self.set_level(self.items[item]['quantity'])

  def add(self, item):
    key, value = item
    self.items[key] = value

  def set_level(self, quantity):
    if quantity <= 10:
      return 'red'
    elif quantity <= 35:
      return 'yellow'
    return 'green'