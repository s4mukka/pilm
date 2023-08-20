from uuid import uuid4

class Product():
  def __init__(self, version, requirements):
    self.id = str(uuid4())
    self.version =  version
    self.requirements = requirements

  def get_tuple(self):
    return (
      self.id,
      {
        "version": self.version,
        "requirements": self.requirements
      }
    )
