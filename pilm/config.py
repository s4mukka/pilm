import os
from configparser import ConfigParser

class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(os.getenv('PILM_CONF'))
