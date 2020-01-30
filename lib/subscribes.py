from lib.global_timer import C_GlobalTimer

class C_Message():
    def __init__(self, _payload="", _message_id=0, _target_id=0, _dest_id=0) :
      self.message_id = _message_id
      self.target_id = _target_id
      self.payload = _payload
      self.dest_id = _dest_id
      self.time_stamp = C_GlobalTimer.get_instance().get_time()
      return

class C_MessagePost():
    def __init__(self) :
      self.messages = []
      return
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
    ### messages 
    ###############################################
    def get_messages(self):
      return self.messages
    def add_message(self, _mes):
      self.messages.append(_mes)
    def clear_messages(self):
      self.messages = []
    def draw_messages(self):
      for _message in self.messages:
        print('Message in Post: time [{} [sec]], id [{}], payload [{}]'.format(_message.time_stamp, _message.message_id, _message.payload))


class C_Subscribes():
    def __init__(self, _subscription_list=[]):
      self.subscription_list = _subscription_list
      self.messages = []
      return
    
    def fetch(self, _messages):
      for _message in _messages:
        if _message.message_id in self.subscription_list:
          self.messages.append(_message)

    def register_subscription_id(self, _id):
      for _subsc in self.subscription_list:
        if _subsc == _id:
          print("Error: subscription is is existence")
          return
      self.subscription_list.append(_id)
    
    def draw_messages(self):
      for _message in self.messages:
        print('My message: time [{} [sec]], id [{}], payload [{}]'.format(_message.time_stamp, _message.message_id, _message.payload))

    def clear_messages(self):
      self.messages = []
