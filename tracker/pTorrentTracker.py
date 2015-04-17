from TrackerServer import TrackerServer
from TrackerConstants import *

DEBUG = False

if DEBUG:
    tracker = TrackerServer(LOCALHOST, 6045, DEBUG_SCHEMA, DEBUG_DB)
else:
    tracker = TrackerServer('0.0.0.0', 6045, DB_SCHEMA, NORMAL_DB)
