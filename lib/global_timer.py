from lib.utils import *
import time

class C_GlobalTimer():
    ###############################################
    ### constructor
    ###############################################
    def __init__(self):
        self.start_time = time.time() 
        self.time = 0 
    
     ###############################################
     ### singleton 
     ###############################################
    _instance = None
    def __new__(cls):
      if cls._instance is None:
        cls._instance = super().__new__(cls)
      return cls._instance

    @classmethod
    def get_instance(cls):
      if not cls._instance:
        cls._instance = cls()
      return cls._instance

    ###############################################
    ### timer 
    ###############################################
    def start_time(self):
      self.start_time = time.time()
      return

    def get_time(self):
      self.time = time.time() - self.start_time
      return self.time
