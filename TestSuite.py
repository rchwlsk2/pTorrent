import unittest
from tests import *

# Code to run all test cases found on
# http://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing

test_classes_to_run = [TestFileUtils, TestMetadataFile,
                       TestFileMap, TestFileAssembler]

loader = unittest.TestLoader()

suites_list = []
for test_class in test_classes_to_run:
    suite = loader.loadTestsFromTestCase(test_class)
    suites_list.append(suite)

big_suite = unittest.TestSuite(suites_list)

runner = unittest.TextTestRunner()
results = runner.run(big_suite)
