import sys
from language_parser import LanguageParser
from language_lexer import LanguageLexer

source_file_name = sys.argv[1]
output_file_name = sys.argv[2]
lexer = LanguageLexer()
parser = LanguageParser()
with open(source_file_name, 'r') as source_reader:
    source_code = source_reader.read()

try:
    tokens = lexer.tokenize(source_code)
    result = parser.parse(tokens)

except Exception as e:
    print("Error: "+str(e))
    exit()

with open(output_file_name, 'w') as output_writer:
    output_writer.write(result)