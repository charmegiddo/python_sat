from lib.base_application import P_BaseApplication
from lib.application_manager import C_ApplicationManager, run
from lib.subscribes import C_Message, C_Subscribes, C_MessagePost, C_ExternalPort, C_ExternalPortLists
from lib.utils import *
import numpy as np

class C_TestAdeviceExternalApplication(P_BaseApplication):
  def __init__(self):
    # class information
    _id = 1
    _type = "Normal"
    _name = "TestA Application"
    _priority = 0
    _dbg_level = DBG_LEVEL_NOTICE 
    super().__init__(_id, _name, _type, _priority, _dbg_level)

  def initialization(self):
    port = C_ExternalPort(100, 0, "UART_A", '/dev/ttyS0', 115200, 0.5)
    C_ExternalPortLists.get_instance().register(port)
    C_ExternalPortLists.get_instance().establish_session()
    self.subscribes.register_subscription_id(1) 

  def fixed_update(self):
    # confirm message
    self.subscribes.draw_messages()
    self.subscribes.clear_messages() 

  def late_update(self):
    if self.local_count % 10 == 0:
      # message, message_id, app_id, target device
      mes = C_Message("Hello from A device", 1, 1, 100) # external
      C_MessagePost.get_instance().add_message(mes)

    if self.local_count % 30 == 0:
      mes = C_Message("Please response", 1, 1, 100)
      C_MessagePost.get_instance().add_message(mes)

class C_TestBdeviceExternalApplication(P_BaseApplication):
  def __init__(self):
    # class information
    _id = 1
    _type = "Normal"
    _name = "TestB Application"
    _priority = 0
    _dbg_level = DBG_LEVEL_NOTICE 
    super().__init__(_id, _name, _type, _priority, _dbg_level)

  def initialization(self):
    port = C_ExternalPort(101, 0, "UART_A", '/dev/ttyS0', 115200, 0.5)
    C_ExternalPortLists.get_instance().register(port)
    C_ExternalPortLists.get_instance().establish_session()
    self.subscribes.register_subscription_id(1) 

  def fixed_update(self):
    # confirm message
    self.subscribes.draw_messages()
    if "response" in self.subscribes.get_latest_message_payload() :
      mes = C_Message("Respond from B device", 1, 1, 101) # external
      C_MessagePost.get_instance().add_message(mes)
    self.subscribes.clear_messages() 

  def late_update(self):
    if self.local_count % 10 == 0:
      # message, message_id, app_id, target device
      mes = C_Message("Hello from B device", 1, 1, 101) # external
      C_MessagePost.get_instance().add_message(mes)


class C_Test1Application(P_BaseApplication):
  def __init__(self):
    # class information
    _type = "Normal"
    _name = "Test1 Application"
    _priority = 0
    _dbg_level = DBG_LEVEL_NOTICE 
    super().__init__(_name, _type, _priority, _dbg_level)

  def fixed_update(self):
    # confirm message
    self.subscribes.draw_messages()
    self.subscribes.clear_messages() 

  def late_update(self):
    mes = C_Message("This message that id is number 1, send from Test1 Application", 1, 0, 0)
    C_MessagePost.get_instance().add_message(mes)
    mes = C_Message("This message that id is number 2, send from Test1 Application", 2, 0, 0)
    C_MessagePost.get_instance().add_message(mes)


class C_Test2Application(P_BaseApplication):
  def __init__(self):
    # class information
    _id = 2
    _type = "Normal"
    _name = "Test2 Application"
    _priority = 1
    _dbg_level = DBG_LEVEL_NOTICE 
    super().__init__(_id, _name, _type, _priority, _dbg_level)
  
  def initialization(self):
    # draw application list
    C_ApplicationManager.get_instance().draw_application_list()
    # register message id
    self.subscribes.register_subscription_id(1) 

  def fixed_update(self):
    # confirm message
    self.subscribes.draw_messages()
    self.subscribes.clear_messages() 
 
  def update(self):
    if self.local_count == 5: 
      # create instance
      C_ApplicationManager.get_instance().register_application(C_Test3Application())
      C_ApplicationManager.get_instance().draw_application_list()
      # register subscription id:2   
      self.subscribes.register_subscription_id(2) 
  
  def late_update(self):
    mes = C_Message("This message that id is number 3, send from Test1 Application", 3, 0, 0)
    C_MessagePost.get_instance().add_message(mes)

  def destroy(self):
    print("Good bye !")

class C_Test3Application(P_BaseApplication):
  def __init__(self):
    # class information
    _id = 3
    _type = "Normal"
    _name = "Test3 Application"
    _priority = 3
    _dbg_level = DBG_LEVEL_NOTICE 
    super().__init__(_id, _name, _type, _priority, _dbg_level)
  
  
  def fixed_update(self):
    # confirm message
    self.subscribes.draw_messages()
    self.subscribes.clear_messages() 

  def update(self):
    if self.local_count == 5:
      C_ApplicationManager.get_instance().remove_application(C_Test2Application())

  def late_update(self):
    mes = C_Message("This is broadcast message, I'm Test3.", 0, 0, 0)
    C_MessagePost.get_instance().add_message(mes)

