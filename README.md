[![Build Status](https://travis-ci.org/jeansberg/PythonVMTranslator.svg?branch=master)](https://travis-ci.org/jeansberg/PythonVMTranslator)
# PythonVMTranslator
This is a virtual machine translator for the VM language defined in *From NAND to Tetris Building a Modern Computer From First Principles* (http://nand2tetris.org/)

It is a console application written in Python.

## Operation
Execute VmTranslator.py with a command line parameter specifying the path to the .vm file you want to translate. The resulting .asm file will be saved in the same folder.

## Tests
Run TranslationTests.py from a test runner to translate the .vm files in the "Test files" directory and compare the resulting .asm file with the corresponding .cmp file. The .cmp files have been verified with the Hack CPU emulator.
