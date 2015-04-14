from file_manager.FileUtils import FileUtils
import CONSTANTS
import unittest
import os
import shutil
import filecmp

class TestFileUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_file_compression(self):
        out_file = "tests/file_manager_tests/data/a.zip"
        if os.path.exists(out_file):
            os.remove(out_file)

        self.assertFalse(os.path.exists(out_file), "File exists prior to test")

        FileUtils.compress_file("tests/file_manager_tests/data/a.txt", out_file)
        self.assertTrue(os.path.exists(out_file), "File does not exist after test")

        os.remove(out_file)

        return

    def test_folder_compression(self):
        out_file = "tests/file_manager_tests/data/dir.zip"
        if os.path.exists(out_file):
            os.remove(out_file)

        self.assertFalse(os.path.exists(out_file), "File exists prior to test")

        FileUtils.compress_file("tests/file_manager_tests/data/dir", out_file)
        self.assertTrue(os.path.exists(out_file), "File does not exist after test")

        os.remove(out_file)

        return

    def test_file_decompression(self):
        zip_file = "tests/file_manager_tests/data/a.zip"
        out_dir = "tests/file_manager_tests/data/aout"

        if os.path.exists(zip_file):
            os.remove(zip_file)
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

        self.assertFalse(os.path.exists(out_dir) and os.path.exists(zip_file), "File(s) exists prior to test")

        FileUtils.compress_file("tests/file_manager_tests/data/a.txt", zip_file)
        FileUtils.decompress_file(zip_file, out_dir)
        self.assertTrue(os.path.exists(out_dir), "Dir does not exist after test")
        self.assertTrue(os.path.exists(out_dir + "/tests/file_manager_tests/data/a.txt"),
                        "File a does not exist after test")
        self.assertTrue(filecmp.cmp("tests/file_manager_tests/data/a.txt",
                                    out_dir + "/tests/file_manager_tests/data/a.txt"), "Files are not the same")

        os.remove(zip_file)
        shutil.rmtree(out_dir)

        return

    def test_folder_decompression(self):
        zip_file = "tests/file_manager_tests/data/dir.zip"
        out_dir = "tests/file_manager_tests/data/dirout"

        if os.path.exists(zip_file):
            os.remove(zip_file)
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

        self.assertFalse(os.path.exists(out_dir) and os.path.exists(zip_file), "File(s) exists prior to test")

        FileUtils.compress_file("tests/file_manager_tests/data/dir", zip_file)
        FileUtils.decompress_file(zip_file, out_dir)

        self.assertTrue(os.path.exists(out_dir) and os.path.isdir(out_dir), "Dir does not exist after test")
        self.assertTrue(os.path.exists(out_dir + "/tests/file_manager_tests/data/dir/b.txt"),
                        "File b does not exist after test")
        self.assertTrue(os.path.exists(out_dir + "/tests/file_manager_tests/data/dir/c.txt"),
                        "File c does not exist after test")

        self.assertTrue(filecmp.cmp("tests/file_manager_tests/data/dir/b.txt",
                                    out_dir + "/tests/file_manager_tests/data/dir/b.txt"),
                        "File b is not the same")
        self.assertTrue(filecmp.cmp("tests/file_manager_tests/data/dir/c.txt",
                                    out_dir + "/tests/file_manager_tests/data/dir/c.txt"),
                        "File c is not the same")

        os.remove(zip_file)
        shutil.rmtree(out_dir)

        return

