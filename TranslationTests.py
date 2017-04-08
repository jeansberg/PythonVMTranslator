import unittest
import os
import sys
import VMTranslator

class VMTranslatorTests(unittest.TestCase):
    def setUp(self):
        self.test_directory = "Test files/"
        self.target_name = ""

    def tearDown(self):
        self.compare_output()
        os.remove(self.test_directory + os.path.splitext(self.target_name)[0] + ".asm")

    def compare_output(self):
        if os.path.splitext(self.target_name)[1] == "":
            self.target_name = os.path.join(self.target_name, os.path.split(self.target_name)[1])

        output_file = open(self.test_directory + os.path.splitext(self.target_name)[0] + ".asm")
        output_data = output_file.read()

        compare_file = open(self.test_directory + os.path.splitext(self.target_name)[0] + ".cmp")
        compare_data = compare_file.read()
        
        self.assertEqual(output_data, compare_data)

    def test_BasicTest_isTranslatedCorrectly(self):
        self.target_name = "BasicTest.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

    def test_PointerTest_isTranslatedCorrectly(self):
        self.target_name = "PointerTest.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

    def test_StaticTest_isTranslatedCorrectly(self):
        self.target_name = "StaticTest.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

    def test_SimpleAdd_isTranslatedCorrectly(self):
        self.target_name = "SimpleAdd.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

    def test_StackTest_isTranslatedCorrectly(self):
        self.target_name = "StackTest.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

    def test_BasicLoop_isTranslatedCorrectly(self):
        self.target_name = "BasicLoop.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

    def test_FibonacciSeries_isTranslatedCorrectly(self):
        self.target_name = "FibonacciSeries.vm"
        VMTranslator.translate(self.test_directory + self.target_name)
        
    def test_SimpleFunction_isTranslatedCorrectly(self):
        self.target_name = "SimpleFunction.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

    def test_NestedCall_isTranslatedCorrectly(self):
        self.target_name = "Sys.vm"
        VMTranslator.translate(self.test_directory + self.target_name)

suite = unittest.TestLoader().loadTestsFromTestCase(VMTranslatorTests)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())