"""Contains test code for the VMTranslator class"""
import unittest
import os
import VMTranslator

class VMTranslatorTests(unittest.TestCase):
    """Tests the entire VMTranslator application by comparing output to existing files"""
    def setUp(self):
        self.translator = VMTranslator.VMTranslator
        self.test_directory = "Test files/"
        self.file_name = ""

    def tearDown(self):
        self.compare_output()
        os.remove(self.test_directory + self.file_name.replace(".vm", ".asm"))

    def compare_output(self):
        """Compare the contents of a generated file with an existing file"""
        output_file = open(self.test_directory + self.file_name.replace(".vm", ".asm"))
        output_data = output_file.read()

        compare_file = open(self.test_directory + self.file_name.replace(".vm", ".cmp"))
        compare_data = compare_file.read()

        self.assertEqual(output_data, compare_data)

    def test_BasicTest_isTranslatedCorrectly(self):
        """Test that the BasicTest virtual machine code is translated properly"""
        self.file_name = "BasicTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_PointerTest_isTranslatedCorrectly(self):
        """Test that the PointerTest virtual machine code is translated properly"""
        self.file_name = "PointerTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_StaticTest_isTranslatedCorrectly(self):
        """Test that the StaticTest virtual machine code is translated properly"""
        self.file_name = "StaticTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_SimpleAdd_isTranslatedCorrectly(self):
        """Test that the SimpleAdd virtual machine code is translated properly"""
        self.file_name = "SimpleAdd.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_StackTest_isTranslatedCorrectly(self):
        """Test that the StackTest virtual machine code is translated properly"""
        self.file_name = "StackTest.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_BasicLoop_isTranslatedCorrectly(self):
        """Test that the BasicLoop virtual machine code is translated properly"""
        self.file_name = "BasicLoop.vm"
        self.translator.translate(self.test_directory + self.file_name)

    def test_FibonacciSeries_isTranslatedCorrectly(self):
        """Test that the FibonacciSeries virtual machine code is translated properly"""
        self.file_name = "FibonacciSeries.vm"
        self.translator.translate(self.test_directory + self.file_name)

suite = unittest.TestLoader().loadTestsFromTestCase(VMTranslatorTests)
unittest.TextTestRunner(verbosity=2).run(suite)
