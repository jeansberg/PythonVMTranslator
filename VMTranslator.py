import os
from os.path import *
import sys
import Generator
import Parser

def get_file_content(filename):
    file = open(filename, "r")
    contents = Parser.parse(file.readlines())
    file.close()
    return (splitext(split(filename)[1])[0], contents)

def translate(target):

    filenames = []
    output_path = splitext(target)[0] + ".asm"

    if isdir(target):
        filenames = filter(lambda entry: isfile(entry) and splitext(entry)[1] == ".vm",
                            [join(target, entry) for entry in os.listdir(target)])
        output_path = join(target, output_path)
    elif isfile(target):
        filenames.append(target)

    generator = Generator.Generator()

    vm_files = dict(map(get_file_content, filenames))
        
    assemblycode_string = generator.generate(vm_files)

    output_file = open(output_path, "w")
    output_file.write(assemblycode_string)
    output_file.close()

if __name__ == '__main__':
    if len(sys.argv) !=2:
        quit("Usage: VMTranslator <fileName.vm> or VMTranslator <directoryName>")
        
    target = sys.argv[1]

    if exists(target):
        translate(target)