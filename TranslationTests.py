import unittest
import os
import VMTranslator

class VMTranslatorTests(unittest.TestCase):
    def setUp(self):
        self.translator = VMTranslator.VMTranslator
        self.test_directory = "Test files/"
        self.file_name = ""

    def tearDown(self):
        self.compare_output()
        os.remove(self.test_directory + self.file_name.replace(".vm", ".asm"))

    def compare_output(self):
        output_file = open(self.test_directory + self.file_name.replace(".vm", ".asm"))
        output_data = output_file.read()

        compare_file = open(self.test_directory + self.file_name.replace(".vm", ".cmp"))
        compare_data = compare_file.read()
        
        self.assertEqual(output_data, compare_data)

    def test_BasicTest_isTranslatedCorrectly(self):
        self.file_name = "BasicTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_PointerTest_isTranslatedCorrectly(self):
        self.file_name = "PointerTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_StaticTest_isTranslatedCorrectly(self):
        self.file_name = "StaticTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_SimpleAdd_isTranslatedCorrectly(self):
        self.file_name = "SimpleAdd.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_StackTest_isTranslatedCorrectly(self):
        self.file_name = "StackTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_BasicLoop_isTranslatedCorrectly(self):
        self.file_name = "BasicLoop.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_FibonacciSeries_isTranslatedCorrectly(self):
        self.file_name = "FibonacciSeries.vm"
        self.translator.translate(self.test_directory + self.file_name)

suite = unittest.TestLoader().loadTestsFromTestCase(VMTranslatorTests)
unittest.TextTestRunner(verbosity=2).run(suite)