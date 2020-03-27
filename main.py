from lib.application_manager import C_ApplicationManager, run
from app.applications import C_Test1Application, C_Test2Application
# entry point
if __name__ == '__main__':
#  run([C_Test1Application(), C_Test2Application()])
  run([C_TestAdeviceExternalApplication()])
