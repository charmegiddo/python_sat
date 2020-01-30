# 0. introduction
This repository consists of software library/sample code that simplifies smallsat development.

Includes the following features:
 - Common state
 - Subscribe communication
 - Task management
 - Debuggging by level

Todo:
 - Serialize
 - Modularized

# 1. Environment and Dependency
 - python 3.8.0
 - numpy 1.16.0

# 2. Implementation
The code you need to develop is at `./app`.
The status flow is as follows:
`__init__` -> `initialization` -> `fixed_update` -> `update` -> `late_update` -> `destroy`

`__init__` is called a once when the class generated.
`initialization` can be called any number of times.
`fixed_update` handles message receive processing.
`update` handles main processing.
`late_update` handles message transmit processing.

## sample
Here are the easiest ways to use the library:

```
class C_Test2Application(P_BaseApplication):
  def __init__(self):
    # class information
    _type = "Normal"
    _name = "Test2 Application"
    _priority = 1
    _dbg_level = DBG_LEVEL_NOTICE 
    super().__init__(_name, _type, _priority, _dbg_level)
  
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

```
