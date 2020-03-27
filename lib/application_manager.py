from lib.base_application import P_BaseApplication
from lib.utils import *
from lib.global_timer import C_GlobalTimer
from lib.subscribes import C_Message, C_Subscribes, C_MessagePost
import numpy as np
import time
class C_ApplicationManager():
    ###############################################
    ### constructor
    ###############################################
    def __init__(self, _invoke_list=[]):
      self.invoke_list = _invoke_list
      self.sort_application()
      self.global_count = 0
      return

    def application_initializer(self):
      for _app in self.invoke_list:
        _app.initialization_manager()
      return
    ###############################################
    ### singleton 
    ###############################################
    _instance = None
    def __new__(cls, _invoke_list=[]):
      if cls._instance is None:
        cls._instance = super().__new__(cls)
      return cls._instance
    @classmethod
    def get_instance(cls):
      if not cls._instance:
        cls._instance = cls()
      return cls._instance

    ###############################################
    ### priority 
    ###############################################
    def sort_application(self):
      # correct priority
      _priori = []
      for _app in self.invoke_list:
        _priori.append(_app.priority)
      # sort idx
      sort_idx = np.asarray(_priori).argsort()
      # sort application
      _new_invoke_list = []
      for _idx in sort_idx:
        _new_invoke_list.append(self.invoke_list[_idx])
      self.invoke_list = _new_invoke_list
      return 
    def register_application(self, _new_application):
      # correct priority
      _priori = []
      for _app in self.invoke_list:
        _priori.append(_app.priority)
        if _app == _new_application:
         draw_dbg('Error [ApplicationManager]: {} is existence'.format(_new_application.class_name), 10, DBG_LEVEL_INFORMATION)
         return
      # sort idx
      sort_idx = np.asarray(_priori).argsort()
      # sort application
      _new_invoke_list = []
      added_flag = 0
      # adding to during of array
      for _idx in sort_idx:
        if _new_application.priority < self.invoke_list[_idx].priority:
          _new_invoke_list.append(_new_application)
          added_flag = 1
        _new_invoke_list.append(self.invoke_list[_idx])
      # adding to end of array
      if added_flag == 0:
        _new_invoke_list.append(_new_application)
      # convert
      self.invoke_list = _new_invoke_list
      _new_application.initialization_manager()
      return 
    def remove_application(self, _target_application):
      for i in range(len(self.invoke_list)):
        _app = self.invoke_list[i]
        if _app == _target_application:
          del self.invoke_list[i]
          _target_application.destroy_manager()
          return
      return
    ###############################################
    ### subscription 
    ###############################################
    def recieve_external_post(self):
      C_MessagePost.get_instance().recieve_external_post()
      return

    def fetch_subscription(self):
      all_messages = C_MessagePost.get_instance().get_messages()
      for _app in self.invoke_list:
        # providing a message
        _app.fetch_message(all_messages)

      C_MessagePost.get_instance().clear_messages()
      return

    def transfer_external_post(self):
      C_MessagePost.get_instance().transfer_external_post()
      return
    ###############################################
    ### update 
    ###############################################
    def update(self):
      for _app in self.invoke_list:
        _app.update_manager()
      self.global_count += 1
      return

    ###############################################
    ### debug 
    ###############################################
    def draw_application_list(self):
      print("----------------application list--------------------")
      print("[priority] application_name")
      for _app in self.invoke_list:
        print('[{}] {}'.format(_app.priority, _app.class_name))
      print("----------------------------------------------------")
      return

def run(_application_list=[]):
  global_timer = C_GlobalTimer()
  print("Launched program...")

  application_manager = C_ApplicationManager(_application_list)
  application_manager.application_initializer()
  
  while True:
    # time
    local_start_time = time.time()
    # subscription recieve
    application_manager.recieve_external_post()
    # subscription fetch
    application_manager.fetch_subscription()
    # update
    application_manager.update()
    # subscription sends
    application_manager.transfer_external_post()

    # wait
    local_time = time.time() - local_start_time
    wait_time = THROUGHOUT_PUT_TIME - local_time
    if (wait_time) > 0:
      time.sleep(wait_time)
    else:
      print("Error: out of time")
    # draw debug information
    local_time = time.time() - local_start_time
    global_time = global_timer.get_instance().get_time()
    draw_dbg('Global time: {} [sec], Local time: {} [sec], Program counter: {}'.format(global_time, local_time, application_manager.global_count), 10, DBG_LEVEL_INFORMATION)

