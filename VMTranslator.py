import sys
import Generator
import Parser

class VMTranslator:

    def translate(file_name):
        parser = Parser.Parser()
        generator = Generator.Generator()

        input_file = open(file_name, "r")
        vmcode_lines = parser.parse(input_file.readlines())
        input_file.close()
        assemblycode_string = generator.generate(vmcode_lines)

        output_name = file_name.replace(".vm", ".asm")
        output_file = open(output_name, "w")
        output_file.write(assemblycode_string)
        output_file.close()

    if __name__ == '__main__':
        if len(sys.argv) != 2 or not sys.argv[1].endswith(".vm"):
            quit("Usage: VMTranslator <fileName.vm>")

        translate(sys.argv[1])