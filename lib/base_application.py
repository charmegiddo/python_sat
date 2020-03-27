from lib.utils import *
from lib.subscribes import C_Message, C_Subscribes

class P_BaseApplication():
    ###############################################
    ### constructor
    ###############################################
    def __init__(self, _id=None, _name=None, _type=None, _priority=None, _dbg_level=1):
        self.app_id = _id 
        self.class_name = _name 
        self.type = _type
        self.priority = _priority
        self.dbg_level = _dbg_level
        self.local_count = 0
        self.subscribes = C_Subscribes([MESSAGE_BROADCAST_ID])
        draw_dbg('Construction [{}]'.format(self.class_name), self.dbg_level, DBG_LEVEL_INFORMATION)
    
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
    ### subscribes 
    ###############################################
    def fetch_message(self, _messages):
      # correct own message
      self.subscribes.fetch(_messages)

    ###############################################
    ### cmmon states
    ###############################################
    def initialization(self):
      return
    def initialization_manager(self):
      draw_dbg('Called method [{}]: initialization()'.format(self.class_name), self.dbg_level, DBG_LEVEL_INFORMATION)
      self.initialization()
    def destroy(self):
      return
    def destroy_manager(self):
      draw_dbg('Called method [{}]: destroy()'.format(self.class_name), self.dbg_level, DBG_LEVEL_INFORMATION)
      self.destroy()
    def update(self):
      return
    def fixed_update(self):
      return
    def late_update(self):
      return
    def update_manager(self):
      draw_dbg('Called method [{}]: fixed_update()'.format(self.class_name), self.dbg_level, DBG_LEVEL_NOTICE)
      self.fixed_update()
      draw_dbg('Called method [{}]: update()'.format(self.class_name), self.dbg_level, DBG_LEVEL_NOTICE)
      self.update()
      draw_dbg('Called method [{}]: late_update()'.format(self.class_name), self.dbg_level, DBG_LEVEL_NOTICE)
      self.late_update()
      self.local_count += 1

    def draw_class_name(self):
        print('Class Name: {}'.format(self.class_name))
    def darw_module_name(self):
        print('Module Name: {}'.format(__name__))
    def darw_parameter_name(self):
        print('Module Name: {}'.format(__name__))
