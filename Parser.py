"""Contains code for parsing virtual machine code"""

class Parser:
    """Parses virtual machine code into pure code lines"""
    def parse(self, lines):
        """Parse a list of strings and return a list with comment lines and line breaks removed"""
        lines = [line.strip("\n") for line in lines if line.strip() != '' and line[0] != '/']
        return lines
