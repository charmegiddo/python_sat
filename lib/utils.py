###############################################
### PROCESSING TIME
###############################################
THROUGHOUT_PUT_TIME = 0.2 # sec

###############################################
### MESSAGE ID
###############################################
MESSAGE_BROADCAST_ID = 0

###############################################
### DEBUG
###############################################
DBG_LEVEL_NOTICE = 2
DBG_LEVEL_INFORMATION = 1
DBG_LEVEL_WARNING = 0

def draw_dbg(_str, _dbg_level=0, _require_dbg_level=0):
  if _dbg_level >= _require_dbg_level:
    print(_str)
  return

