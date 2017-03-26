class Parser:
    def parse(self, lines):
        lines = [line.strip("\n") for line in lines if line.strip() != '' and line[0] != '/']
        return lines