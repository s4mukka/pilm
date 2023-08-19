class Stock:
  def __init__(self):
    self.items = self.start_stock(range(100))

  def start_stock(sefl, items_type):
    return {item_type: 50 for item_type in items_type}

  def see_stock(self, item):
    return self.items[item]
  
  def has_stock(self, items):
    for item, quantity in items.items():
      if item not in self.items:
        return False
      if self.items[item] < quantity:
        return False
    return True
  
  def consume_stock(self, items):
    for item, quantity in items.items():
      self.items[item] -= quantity

  def add(self, item):
    name, quantity = item
    self.items[name] = quantity
