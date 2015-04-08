import unittest
from file_manager import FileMap


##
# Tests the basic functionality of the file map
#
# @author Paul Rachwalski
# @date Apr 5, 2015
##
class TestFileMap(unittest.TestCase):

    def setUp(self):
        pass

    ##
    # Test that initial values of variables are correct
    ##
    def test_constructor(self):
        map = FileMap("name", 16, 2)

        self.assertEqual(map.filename, "name", "Incorrect map file name")
        self.assertEqual(map.size, 16, "Incorrect map size")
        self.assertEqual(map.bits, 8, "Incorrect number of map sections")
        self.assertIsNone(map.map, "Incorrect value of map")
        self.assertEqual(len(map.in_progress), 0, "Incorrect number of entries in map progress list")

        return

    ##
    # Test that create assigns the correct amount of space for the bytearray and that the values are zero
    ##
    def test_create(self):
        map = FileMap("name", 16, 2)
        map.create()

        self.assertEqual(len(map.map), 1, "Incorrect map length")
        self.assertEqual(map.map[0], 0, "Map is not null")

        map = FileMap("name", 64, 4)
        map.create()

        self.assertEqual(len(map.map), 2, "Incorrect map length")
        self.assertTrue(map.map[0] == map.map[1] == 0, "Map is not null")

        return

    ##
    # Tests the persistence functions of the file map
    ##
    def test_persistence(self):
        filename = "name.ptmap"
        map = FileMap(filename, 16, 2)
        map.create()

        self.assertEqual(len(map.map), 1, "Incorrect initial map length")
        self.assertEqual(map.map[0], 0, "Initial map is not null")
        map.save()

        mapb = FileMap(filename, 16, 2)
        mapb.load()
        self.assertEqual(len(mapb.map), 1, "Incorrect map length")
        self.assertEqual(mapb.map[0], 0, "Map is not null")

        return

    ##
    # Tests that setting bits works properly
    ##
    def test_bit_marking(self):
        filename = "name.ptmap"
        map = FileMap(filename, 16, 2)
        map.create()

        map.set_in_progress(3)
        map.set_in_progress(5)
        self.assertTrue(3 in map.in_progress and 5 in map.in_progress, "Incorrect values in map's progress")

        map.set_complete(3)
        self.assertTrue(5 in map.in_progress, "Incorrect values in map's progress")
        self.assertEqual(map.map[0], 8, "Incorrect value of map bits")

        return

    ##
    # Tests the completion of an even sized file map
    ##
    def test_complete_even(self):
        filename = "name.ptmap"
        map = FileMap(filename, 16, 2)
        map.create()

        map.set_in_progress(0)
        map.set_in_progress(1)
        map.set_in_progress(2)
        map.set_in_progress(3)
        map.set_in_progress(4)
        map.set_in_progress(5)
        map.set_in_progress(6)
        map.set_in_progress(7)

        all_in_progress = True
        for i in range(0, 8):
            if i not in map.in_progress:
                all_in_progress = False
                break
        self.assertTrue(all_in_progress, "Incorrect values in map's progress")


        map.set_complete(3)
        all_in_progress = True
        for i in range(0, 8):
            if i not in map.in_progress:
                all_in_progress = False
                break
        self.assertFalse(all_in_progress, "Incorrect values in map's progress")
        self.assertEqual(map.map[0], 8, "Incorrect value of map bits")
        self.assertFalse(map.is_complete(), "Incorrect completion value")

        map.set_complete(0)
        map.set_complete(1)
        map.set_complete(2)
        map.set_complete(4)
        map.set_complete(5)
        map.set_complete(6)
        map.set_complete(7)
        self.assertTrue(map.is_complete(), "Incorrect completion value")

        return

    ##
    # Tests the completion of an odd sized file map
    ##
    def test_complete_odd(self):
        filename = "name.ptmap"
        map = FileMap(filename, 12, 2)
        map.create()

        map.set_in_progress(0)
        map.set_in_progress(1)
        map.set_in_progress(2)
        map.set_in_progress(3)
        map.set_in_progress(4)
        map.set_in_progress(5)

        all_in_progress = True
        for i in range(0, 6):
            if i not in map.in_progress:
                all_in_progress = False
                break
        self.assertTrue(all_in_progress, "Incorrect values in map's progress")


        map.set_complete(3)
        all_in_progress = True
        for i in range(0, 8):
            if i not in map.in_progress:
                all_in_progress = False
                break
        self.assertFalse(all_in_progress, "Incorrect values in map's progress")
        self.assertEqual(map.map[0], 8, "Incorrect value of map bits")
        self.assertFalse(map.is_complete(), "Incorrect completion value")

        map.set_complete(0)
        map.set_complete(1)
        map.set_complete(2)
        map.set_complete(4)
        map.set_complete(5)
        self.assertTrue(map.is_complete(), "Incorrect completion value")

        return


    ##
    # Tests the recommendation function
    ##
    def test_recommend(self):
        filename = "name.ptmap"
        map = FileMap(filename, 12, 2)
        map.create()

        self.assertEqual(map.recommend_piece(), 0, "Incorrect initial recommendation")

        map.set_in_progress(0)
        map.set_in_progress(1)
        map.set_in_progress(2)
        self.assertEqual(map.recommend_piece(), 3, "Incorrect in progress recommendation")

        map.set_complete(0)
        map.set_complete(1)
        map.set_complete(2)
        map.set_in_progress(3)
        self.assertEqual(map.recommend_piece(), 4, "Incorrect complete/in progress recommendation")


        map.set_in_progress(4)
        map.set_in_progress(5)
        map.set_in_progress(6)
        map.set_in_progress(7)
        map.set_complete(3)
        map.set_complete(4)
        map.set_complete(5)
        map.set_complete(6)
        map.set_complete(7)
        self.assertEqual(map.recommend_piece(), -1, "Incorrect complete map recommendation")

        return