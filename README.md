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

# 2. Usage

```
$ python main.py
```

Running result is the following:

```
Construction [Test1 Application]
Construction [Test2 Application]
Launched program...
Called method [Test1 Application]: initialization()
Called method [Test2 Application]: initialization()
----------------application list--------------------
[priority] application_name
[0] Test1 Application
[1] Test2 Application
----------------------------------------------------
Called method [Test1 Application]: fixed_update()
Called method [Test1 Application]: update()
Called method [Test1 Application]: late_update()
Called method [Test2 Application]: fixed_update()
Called method [Test2 Application]: update()
Called method [Test2 Application]: late_update()
Global time: 0.20037198066711426 [sec], Local time: 0.20025897026062012 [sec], Program counter: 1
Called method [Test1 Application]: fixed_update()
Called method [Test1 Application]: update()
Called method [Test1 Application]: late_update()
Called method [Test2 Application]: fixed_update()
My message: time [0.00014829635620117188 [sec]], id [1], payload [This message that id is number 1, send from Test1 Application]
Called method [Test2 Application]: update()
Called method [Test2 Application]: late_update()
Global time: 0.4007713794708252 [sec], Local time: 0.2003011703491211 [sec], Program counter: 2
Called method [Test1 Application]: fixed_update()
Called method [Test1 Application]: update()
Called method [Test1 Application]: late_update()
Called method [Test2 Application]: fixed_update()
My message: time [0.20053887367248535 [sec]], id [1], payload [This message that id is number 1, send from Test1 Application]
Called method [Test2 Application]: update()
Called method [Test2 Application]: late_update()
Global time: 0.6012277603149414 [sec], Local time: 0.20030617713928223 [sec], Program counter: 3
Called method [Test1 Application]: fixed_update()
Called method [Test1 Application]: update()
Called method [Test1 Application]: late_update()
Called method [Test2 Application]: fixed_update()
My message: time [0.40101099014282227 [sec]], id [1], payload [This message that id is number 1, send from Test1 Application]
Called method [Test2 Application]: update()
Called method [Test2 Application]: late_update()
Global time: 0.8016915321350098 [sec], Local time: 0.2003030776977539 [sec], Program counter: 4
Called method [Test1 Application]: fixed_update()
Called method [Test1 Application]: update()
Called method [Test1 Application]: late_update()
Called method [Test2 Application]: fixed_update()
My message: time [0.6015028953552246 [sec]], id [1], payload [This message that id is number 1, send from Test1 Application]
Called method [Test2 Application]: update()
Called method [Test2 Application]: late_update()
Global time: 1.0021541118621826 [sec], Local time: 0.2003180980682373 [sec], Program counter: 5
Called method [Test1 Application]: fixed_update()
Called method [Test1 Application]: update()
Called method [Test1 Application]: late_update()
Called method [Test2 Application]: fixed_update()
My message: time [0.8018946647644043 [sec]], id [1], payload [This message that id is number 1, send from Test1 Application]
Called method [Test2 Application]: update()
Construction [Test3 Application]
Called method [Test3 Application]: initialization()
----------------application list--------------------
[priority] application_name
[0] Test1 Application
[1] Test2 Application
[3] Test3 Application
----------------------------------------------------
Called method [Test2 Application]: late_update()
Global time: 1.202599287033081 [sec], Local time: 0.20027709007263184 [sec], Program counter: 6
Called method [Test1 Application]: fixed_update()
Called method [Test1 Application]: update()
Called method [Test1 Application]: late_update()
Called method [Test2 Application]: fixed_update()
My message: time [1.0024144649505615 [sec]], id [1], payload [This message that id is number 1, send from Test1 Application]
My message: time [1.002420425415039 [sec]], id [2], payload [This message that id is number 2, send from Test1 Application]
Called method [Test2 Application]: update()
Called method [Test2 Application]: late_update()
Called method [Test3 Application]: fixed_update()
Called method [Test3 Application]: update()
Called method [Test3 Application]: late_update()
Global time: 1.4031026363372803 [sec], Local time: 0.20034480094909668 [sec], Program counter: 7
```

The cycle period is 200 ms.

# 3. Implementation
The code you need to develop is at `./app`.

The status flow is as follows:

`__init__` -> `initialization` -> `fixed_update` -> `update` -> `late_update` -> `destroy`

 - `__init__` is called a once when the class generated.
 - `initialization` can be called any number of times.
 - `fixed_update` handles message receive processing.
 - `update` handles main processing.
 - `late_update` handles message transmit processing.

## 3.1. sample
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

Enjoy !
