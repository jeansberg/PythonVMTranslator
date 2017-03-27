"""Contains code for generating Hack assembly code"""

class Generator:
    """Generates assembly code based on virtual machine code"""
    # Memory segment names
    TEMP = "temp"
    STATIC = "static"
    CONSTANT = "constant"

	# Maps VM language memory segment names to assembly symbols
    memory_segments = {'stack': 'SP',
                       'local': 'LCL',
                       'argument': 'ARG',
                       'this': 'THIS',
                       'that': 'THAT'}

	# Memory locations of the temp and static blocks
    memory_locations = {'temp': 5,
                        'static': 16}

	# Arithmetic operations on one operand
    unaryOperations = [
        'not',
        'neg',
    ]

	# Arithmetic operations on two operands
    binaryOperations = [
        'and',
        'or',
        'add',
        'sub',
        'eq',
        'lt',
        'gt'
    ]

	# Types of jump instructions
    jump_instructions = {
        'JEQ',
        'JGT',
        'JLT'
    }

	# Holds the generated code string
    generated_code = ""

	# Keeps track of the number of generated instructions
    instruction_count = 0

    # Disables or enables comments in the generated code
    write_comments = False

    def write_instruction(self, text):
        """Write an instruction to the output string and increment the instruction count"""
        self.generated_code += text + "\n"
        self.instruction_count += 1

    def write_comment(self, text):
        """Write a comment to the output string"""
        if(self.write_comments):
            self.generated_code += "// " + text + "\n"

    def address_memory(self, segment, offset=None):
        """Address some memory"""
        if segment in self.memory_segments:
            self.address_indirect(self.memory_segments[segment], offset)
        elif segment == "pointer":
            if offset == "0":
                self.address_direct("THIS", 0)
            elif offset == "1":
                self.address_direct("THAT", 0)
        elif segment in ("temp", "static"):
            self.address_direct(segment, offset)

    def address_indirect(self, symbol, offset=None):
        """Get the address pointed to by the specified pointer and offset and store it in the A register"""
        self.write_comment("Address {0} {1}".format(symbol, offset))

        # Store pointer location in A register
        self.write_instruction("@{0}".format(symbol))

        # Increment the address pointed to with the offset
        if offset != None:
            for _ in range(0, int(offset)):
                self.write_instruction("M=M+1")

        # Store the address in the A register
        # The value is accessible through M
        self.write_instruction("A=M")

    def address_direct(self, symbol, offset=None):
        """Get the address represented by the specified symbol and offset and store it in the A register"""
        if symbol in self.memory_locations:
            self.write_comment("Address {0} {1}".format(symbol, offset))
            # Store the address in the A register
            # The value is accessible through M
            self.write_instruction("@{0}".format(self.memory_locations[symbol] + int(offset)))
        else:
            # Store the address in the A register
            # The value is accessible through M
            self.write_instruction("@{0}".format(symbol))

    def shift_pointer(self, segment, offset):
        """Increment or decrement the address pointed to by the specified pointer"""
        if abs(int(offset)) == 0:
            return

        self.write_comment("Shift {0} {1}".format(segment, offset))
        self.write_instruction("@{0}".format(self.memory_segments[segment]))

        for _ in range(0, abs(int(offset))):
            if int(offset) > 0:
                self.write_instruction("M=M+1")
            else:
                self.write_instruction("M=M-1")

        self.write_instruction("A=M")

    def generate_push(self, memory_segment, offset):
        """Generate code for a push operation"""
        if memory_segment == self.CONSTANT:
            self.write_instruction("@{0}".format(offset))
            self.write_instruction("D=A")
        else:
            self.address_memory(memory_segment, offset)
            self.write_instruction("D=M")
        self.address_memory("stack")
        self.write_instruction("M=D")
        self.shift_pointer("stack", 1)
        if memory_segment in self.memory_segments:
            # Reset the pointer
            self.shift_pointer(memory_segment, "-{0}".format(offset))

    def generate_pop(self, memory_segment, offset):
        """Generate code for a pop operation"""
        self.shift_pointer("stack", -1)
        self.address_memory("stack")
        self.write_instruction("D=M")
        self.address_memory(memory_segment, offset)
        self.write_instruction("M=D")
        if memory_segment in self.memory_segments:
            # Reset the pointer
            self.shift_pointer(memory_segment, "-{0}".format(offset))

    def generate_arithmetic(self, operation):
        """Generate code for an arithmetic operation"""
        # One operand operations
        if operation in self.unaryOperations:
            self.shift_pointer("stack", -1)
            if operation == "neg":
                self.write_instruction("M=-M")
            elif operation == "not":
                self.write_instruction("M=!M")
        # Two operand operations
        elif operation in self.binaryOperations:
            self.shift_pointer("stack", -1)
            self.write_instruction("D=M")
            self.shift_pointer("stack", -1)
            if operation == "add":
                self.write_instruction("M=M+D")
            elif operation == "sub":
                self.write_instruction("M=M-D")
            elif operation == "or":
                self.write_instruction("M=M|D")
            elif operation == "and":
                self.write_instruction("M=M&D")
            elif operation == "eq":
                self.generate_comparison("JEQ")
            elif operation == "lt":
                self.generate_comparison("JLT")
            elif operation == "gt":
                self.generate_comparison("JGT")

        self.shift_pointer("stack", 1)

    def generate_comparison(self, type_of_jump):
        """Generate code for an comparison operation"""
        self.write_comment("Compare values")
        self.write_instruction("D=M-D")
        self.write_instruction("@{0}".format(self.instruction_count + 7))
        self.write_instruction("D;{0}".format(type_of_jump))
		# Result is false (-1)
        self.address_memory("stack")
        self.write_instruction("M=0")
        self.write_instruction("@{0}".format(self.instruction_count + 5))
        self.write_instruction("D;JMP")
		# Result is true (-1)
        self.address_memory("stack")
        self.write_instruction("M=-1")

    def generate(self, lines_of_code, write_comments=False):
        """Parse a list of code lines and call specialized functions to translate them"""
        self.write_comments = write_comments
        for line in lines_of_code:
            words = line.split(' ')
            self.write_comment("***{0}***".format(line))
            if words[0] == "push":
                self.generate_push(words[1], words[2])
            elif words[0] == "pop":
                self.generate_pop(words[1], words[2])
            elif words[0] in self.unaryOperations + self.binaryOperations:
                self.generate_arithmetic(words[0])
            elif words[0] == "label":
                self.generate_label(words[1])
            elif "goto" in words[0]:
                self.generate_goto(words[0], words[1])
            elif words[0] == "function":
                self.generate_function(words[1], words[2])
            elif words[0] == "return":
                self.generate_return()
            elif words[0] == "call":
                self.generate_call(words[1], words[2])
        return self.generated_code

    def generate_label(self, label):
        """Generate a label"""
        self.write_comment("Generate label {0}".format(label))
        self.write_instruction("({0})".format(label))

    def generate_goto(self, goto_type, label):
        """Generate code for a goto operation"""
        if goto_type == "if-goto":
            self.shift_pointer("stack", -1)
            self.address_memory("stack")
            self.write_instruction("D=M")
            # if D = 0 skip the goto by jumping over it
            self.write_instruction("@{0}".format(self.instruction_count + 3))
            self.write_instruction("D;JEQ")

		# if D != 0 or it is a plain goto, jump to the label
        self.write_instruction("@{0}".format(label))
        self.write_instruction("D;JMP")
