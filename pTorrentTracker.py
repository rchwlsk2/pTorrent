from tracker import TrackerServer
import CONSTANTS

DEBUG = True

if DEBUG:
    tracker = TrackerServer(CONSTANTS.LOCALHOST, 6044, CONSTANTS.DB_SCHEMA, CONSTANTS.DEBUG_DB)
else:
    tracker = TrackerServer(CONSTANTS.LOCALHOST, 6044, CONSTANTS.DB_SCHEMA, CONSTANTS.NORMAL_DB)