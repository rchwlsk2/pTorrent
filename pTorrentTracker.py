from tracker import TrackerServer
import PATHS

DEBUG = True

if DEBUG:
    tracker = TrackerServer(PATHS.LOCALHOST, 6044, PATHS.DB_SCHEMA, PATHS.DEBUG_DB)
else:
    tracker = TrackerServer(PATHS.LOCALHOST, 6044, PATHS.DB_SCHEMA, PATHS.NORMAL_DB)