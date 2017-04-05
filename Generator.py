class Generator:
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
        self.shift_pointer("stack", -1)
        self.address_memory("stack")
        self.write_instruction("D=M")
        self.address_memory(memory_segment, offset)
        self.write_instruction("M=D")
        if memory_segment in self.memory_segments:
            # Reset the pointer
            self.shift_pointer(memory_segment, "-{0}".format(offset))

    def generate_arithmetic(self, operation):
        """Generate an arithmetic operation"""
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
        self.write_comments = write_comments
                self.generate_push(words[1], words[2])
                self.generate_pop(words[1], words[2])
                self.generate_label(words[1])
            elif "goto" in words[0]:
                self.generate_goto(words[0], words[1])
                self.generate_call(words[1], words[2])


        for file in vm_files:
            for line in vm_files[file]:
                words = line.split(' ')
                self.write_comment("***{0}***".format(line))
                if words[0] == "push":
                elif words[0] == "pop":
                elif words[0] in self.unaryOperations + self.binaryOperations:
                    self.generate_arithmetic(words[0])
                elif words[0] == "label":
                elif words[0] == "function":
                    self.generate_function(words[1], words[2])
                elif words[0] == "return":
                    self.generate_return()
                elif words[0] == "call":

        return self.generated_code

    def generate_label(self, label):
        self.write_comment("Generate label {0}".format(label))
        self.write_instruction("({0})".format(label))

    def generate_goto(self, goto_type, label):
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

    def generate_function(self, name, number_of_arguments):
        # Declare a label for the function entry
        self.generate_label(name)
        # Push local variables initialized to zero
        for _ in range(0, int(number_of_arguments)):
            self.generate_push("constant", 0)

    def generate_call(self, name, number_of_arguments):
        return_label = "Return_{0}".format(name)
        self.write_comment("Push the return address")
        self.write_instruction("@{0}".format(return_label))
        self.write_instruction("D=A")
        self.address_memory("stack")
        self.write_instruction("M=D")
        self.shift_pointer("stack", 1)
        self.write_comment("Save LCL of the calling function")
        self.write_instruction("@LCL")
        self.write_instruction("D=M")
        self.address_memory("stack")
        self.write_instruction("M=D")
        self.shift_pointer("stack", 1)
        self.write_comment("Save ARG of the calling function")
        self.write_instruction("@ARG")
        self.write_instruction("D=M")
        self.address_memory("stack")
        self.write_instruction("M=D")
        self.shift_pointer("stack", 1)
        self.write_comment("Save THIS of the calling function")
        self.write_instruction("@THIS")
        self.write_instruction("D=M")
        self.address_memory("stack")
        self.write_instruction("M=D")
        self.shift_pointer("stack", 1)
        self.write_comment("Save THAT of the calling function")
        self.write_instruction("@THAT")
        self.write_instruction("D=M")
        self.address_memory("stack")
        self.write_instruction("M=D")
        self.shift_pointer("stack", 1)
        self.write_comment("Reposition ARG")
        self.address_direct("SP")
        self.write_instruction("D=M")
        for _ in range(0, int(number_of_arguments) + 5):
            self.write_instruction("D=D-1")
        self.address_direct("ARG")
        self.write_instruction("M=D")
        self.write_comment("Reposition LCL")
        self.address_direct("SP")
        self.write_instruction("D=M")
        self.address_direct("LCL")
        self.write_instruction("M=D")
        self.write_comment("Transfer control")
        self.generate_goto("goto", name)
        self.write_comment("Declare a label for the return address")
        self.generate_label(return_label)

    def generate_return(self):
        # FRAME = LCL (FRAME is a temporary variable stored in R13)
        self.address_memory("local")
        self.write_instruction("D=A")
        self.write_instruction("@R13")
        self.write_instruction("M=D")

        # retaddr = *(frame-5) (stored in R14)
        self.write_instruction("@R13")
        self.write_instruction("D=M")
        for _ in range(0, 5):
            self.write_instruction("D=D-1")

        self.write_instruction("A=D")
        self.write_instruction("D=M")
        self.write_instruction("@R14")
        self.write_instruction("M=D")

        # *ARG = pop
        self.generate_pop("argument", 0)

        # SP = ARG + 1
        self.address_memory("argument")
        self.write_instruction("D=A")
        self.write_instruction("D=D+1")
        self.address_direct("SP")
        self.write_instruction("M=D")

        # THAT = *(frame-1)
        self.write_instruction("@R13")
        self.write_instruction("D=M")
        self.write_instruction("D=D-1")

        self.write_instruction("A=D")
        self.write_instruction("D=M")
        self.address_direct("THAT")
        self.write_instruction("M=D")

        # THIS = *(frame-2)
        self.write_instruction("@R13")
        self.write_instruction("D=M")
        self.write_instruction("D=D-1")
        self.write_instruction("D=D-1")

        self.write_instruction("A=D")
        self.write_instruction("D=M")
        self.address_direct("THIS")
        self.write_instruction("M=D")

        # ARG = *(frame-3)
        self.write_instruction("@R13")
        self.write_instruction("D=M")
        self.write_instruction("D=D-1")
        self.write_instruction("D=D-1")
        self.write_instruction("D=D-1")

        self.write_instruction("A=D")
        self.write_instruction("D=M")
        self.address_direct("ARG")
        self.write_instruction("M=D")

        # LCL = *(frame-4)
        self.write_instruction("@R13")
        self.write_instruction("D=M")
        self.write_instruction("D=D-1")
        self.write_instruction("D=D-1")
        self.write_instruction("D=D-1")
        self.write_instruction("D=D-1")

        self.write_instruction("A=D")
        self.write_instruction("D=M")
        self.address_direct("LCL")
        self.write_instruction("M=D")

        self.write_instruction("@R14")
        self.write_instruction("A=M")
        self.write_instruction("D;JMP")