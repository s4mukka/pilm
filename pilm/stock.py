class Stock:
  def __init__(self):
    self.artefacts = {}

  def see_stock(self, artefact):
    return self.artefacts[artefact]

  def add(self, artefact):
    name, quantity = artefact
    self.artefacts[name] = quantity
