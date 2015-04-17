ROOT = "tracker/"
DEBUG_DB = "tracker/tests/data/tracker.db"
DEBUG_SCHEMA = "tracker/tests/data/schema.sql"

NORMAL_DB = "data/tracker.db"
DB_SCHEMA = "data/schema.sql"

LOCALHOST = ""


##
# Constant values in messages sent by tracker
#
# @author Paul Rachwalski
# @date Apr 2, 2015
##
class TrackerConstants(object):

    CONNECT_SUCCESS = "connected successfully"

    ADD = "add "
    ADD_SUCCESS = "added successfully"
    ADD_FAIL = "add failed"

    REMOVE = "rem "
    REMOVE_SUCCESS = "removed successfully"
    REMOVE_FAIL = "remove failed"

    GET = "get "
    GET_SUCCESS = "got ips successfully"
    GET_FAIL = "get failed"