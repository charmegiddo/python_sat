from lib.global_timer import C_GlobalTimer
import serial
import pickle
import time

class C_ExternalPort():
    def __init__(self, _id=-1, _type=0, _name="", _mapping_port="", _baud_rate=115200, _time_out=0.5):
      self.id = _id
      self.type = _type # 0 is UART
      self.name = _name
      self.mapping_port = _mapping_port
      self.baud_rate = _baud_rate
      self.time_out = _time_out
      self.session = None
      self.recieve_temp_message = b''
      return

class C_ExternalPortLists():
    ###############################################
    ### constructor
    ###############################################
    def __init__(self):
      self.external_ports = []

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
    ### register 
    ###############################################
    def register(self, _port):
      self.external_ports.append(_port)

    def establish_session(self):
      for i in range (len(self.external_ports)):
        # UART
        if self.external_ports[i].type == 0:
          self.external_ports[i].session = serial.Serial(self.external_ports[i].mapping_port, self.external_ports[i].baud_rate, timeout=self.external_ports[i].time_out)
          print('INFO establishment of session: {}'.format(self.external_ports[i].session))
          
    def get_external_ports(self):
      return self.external_ports

    def get_external_port(self, _id):
      for _port in self.external_ports:
        if _port.id == _id:
          return _port
      return 0

    def get_sessions(self):
      session_list = []
      for i in range (len(self.external_ports)):
        if self.external_ports[i].session != None:
          session_list.append(self.external_ports[i])
      return session_list

    def get_existence(self, _id):
      for _port in self.external_ports:
        if _port.id == _id:
          return 1
      return 0


class C_Message():
    def __init__(self, _payload="", _message_id=0, _target_id=0, _dest_id=0) :
      self.payload = _payload
      self.message_id = _message_id # message id
      self.target_id = _target_id # app id
      self.dest_id = _dest_id # device id 
      self.time_stamp = C_GlobalTimer.get_instance().get_time()
      return

class C_MessagePost():
    def __init__(self) :
      self.internal_messages = []
      self.external_messages = []
      self.start_charcter = '__STA__'
      self.end_charcter = '__FIN__'

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
      return self.internal_messages

    def add_message(self, _mes):
      is_external = C_ExternalPortLists.get_instance().get_existence(_mes.dest_id)
      if is_external == 1:
        self.external_messages.append(_mes)  
      else:
        self.internal_messages.append(_mes)

    # External send
    def transfer_external_post(self):
      for mes in self.external_messages:
        port = C_ExternalPortLists.get_instance().get_external_port(mes.dest_id)
        binary_packing = pickle.dumps(mes) # serialize
        binary_packing = self.start_charcter.encode('UTF-8') + binary_packing + self.end_charcter.encode('UTF-8')
        port.session.write(binary_packing) # send
        print('INFO transfer message: {}, {}'.format(port.session, binary_packing))
      self.clear_external_messages()

    # External recieve
    def recieve_external_post(self):
      sess = C_ExternalPortLists.get_instance().get_sessions()
      for i in range(len(sess)):
        recieve_message = sess[i].session.read_all()
        if len(recieve_message) < 1:
          continue

        # during sending data?
        sess[i].recieve_temp_message += recieve_message

        recieve_message = sess[i].recieve_temp_message.split(self.start_charcter.encode('UTF-8'))
        recieve_message = recieve_message[1:] # debri 

        # during sending data? if <S>B... -> tmp = <S>B...
        if self.end_charcter.encode('UTF-8') not in recieve_message[-1]:
          sess[i].recieve_temp_message = self.start_charcter.encode('UTF-8') + recieve_message[-1]
          recieve_message = recieve_message[:-1] # eliminate end data

        for _message in recieve_message: 
          parse = sess[i].recieve_temp_message.strip(self.end_charcter.encode('UTF-8'))
          parse = parse.strip(self.start_charcter.encode('UTF-8'))
          msg = pickle.loads(parse)
          self.internal_messages.append(msg) # save internal messages
          print('INFO recieve external message: {}, {}'.format(sess[i].session, msg))
          
    def clear_external_messages(self):
      self.external_messages = []

    def clear_messages(self):
      self.internal_messages = []

    def draw_messages(self):
      for _message in self.internal_messages:
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
          print("Error: subscription id is existence")
          return
      self.subscription_list.append(_id)

    def get_latest_message_payload(self):
      if len(self.messages) != 0:
        return self.messages[-1].payload
      return ""

    def draw_messages(self):
      for _message in self.messages:
        print('My message: time [{} [sec]], id [{}], payload [{}]'.format(_message.time_stamp, _message.message_id, _message.payload))

    def clear_messages(self):
      self.messages = []
