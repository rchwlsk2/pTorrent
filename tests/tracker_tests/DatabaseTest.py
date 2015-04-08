import unittest
import os
from tracker.DatabaseManager import DatabaseManager


##
# Test the database manager for the tracker server
#
# @author Paul Rachwalski
# @date Apr 2, 2015
##
class TestDatabase(unittest.TestCase):

    DB_PATH = "tests/tracker_tests/data/test_tracker.db"
    DB_SCHEMA = "tests/tracker_tests/data/schema.sql"

    sample_vals = (("abcd", "123.456.8.3"), ("SDFGHS", "123.456.8.3"), ("SDFGHS", "342.455.531.84"))

    def setUp(self):
        pass

    ##
    # Test that the initializer properly creates the database
    ##
    def testConstructor(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

        dbManager = DatabaseManager(self.DB_SCHEMA, self.DB_PATH)
        dbManager.init_db()
        db_conn = dbManager.connect_db()
        db_cursor = db_conn.cursor()

        tracker_exists_query = "SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'tracker'"
        db_cursor.execute(tracker_exists_query)
        self.assertEquals(db_cursor.fetchone()[0], 1, "Incorrect database: 'tracker' table is not created")

        db_conn.close()
        return

    ##
    # Test that entries are properly added to the table
    ##
    def testAdd(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

        dbManager = DatabaseManager(self.DB_SCHEMA, self.DB_PATH)
        dbManager.init_db()
        db_conn = dbManager.connect_db()
        db_cursor = db_conn.cursor()
        dbManager.add(self.sample_vals[0][0], self.sample_vals[0][1])

        add_check_query = "SELECT * FROM tracker"
        db_cursor.execute(add_check_query)
        rows = db_cursor.fetchall()

        self.assertEqual(len(rows), 1, "Incorrect number of entries added to table")
        self.assertEqual(rows[0][0], self.sample_vals[0][0], "Incorrect file id stored")
        self.assertEqual(rows[0][1], self.sample_vals[0][1], "Incorrect ip address stored")

        db_conn.close()
        return

    ##
    # Test that entries are properly removed from the table
    ##
    def testRemove(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

        dbManager = DatabaseManager(self.DB_SCHEMA, self.DB_PATH)
        dbManager.init_db()
        db_conn = dbManager.connect_db()
        db_cursor = db_conn.cursor()
        dbManager.add(self.sample_vals[0][0], self.sample_vals[0][1])
        dbManager.add(self.sample_vals[1][0], self.sample_vals[1][1])
        dbManager.add(self.sample_vals[2][0], self.sample_vals[2][1])

        add_check_query = "SELECT * FROM tracker"
        db_cursor.execute(add_check_query)
        rows = db_cursor.fetchall()
        self.assertEqual(len(rows), 3, "Incorrect number of entries added to table")

        dbManager.remove("*", self.sample_vals[0][1])
        add_check_query = "SELECT * FROM tracker"
        db_cursor.execute(add_check_query)
        rows = db_cursor.fetchall()
        self.assertEqual(len(rows), 1, "Incorrect number of entries removed from table for multiple removal")

        dbManager.remove(self.sample_vals[2][0], self.sample_vals[2][1])
        add_check_query = "SELECT * FROM tracker"
        db_cursor.execute(add_check_query)
        rows = db_cursor.fetchall()
        self.assertEqual(len(rows), 0, "Incorrect number of entries removed from table for single removal")

        return

    ##
    # Test that the list of ip's is properly returned from table
    ##
    def testGet(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

        dbManager = DatabaseManager(self.DB_SCHEMA, self.DB_PATH)
        dbManager.init_db()
        dbManager.add(self.sample_vals[0][0], self.sample_vals[0][1])
        dbManager.add(self.sample_vals[1][0], self.sample_vals[1][1])
        dbManager.add(self.sample_vals[2][0], self.sample_vals[2][1])

        ip_list = dbManager.get(self.sample_vals[1][0])
        self.assertEqual(len(ip_list), 2, "Incorrect number of IPs found for multiple get")
        self.assertTrue(self.sample_vals[1][1] in ip_list, "First IP not in IP list")
        self.assertTrue(self.sample_vals[2][1] in ip_list, "Second IP not in IP list")

        ip_list = dbManager.get(self.sample_vals[0][0])
        self.assertEqual(len(ip_list), 1, "Incorrect number of IPs found for single get")
        self.assertTrue(self.sample_vals[0][1] in ip_list, "Only IP not in IP list")

        return