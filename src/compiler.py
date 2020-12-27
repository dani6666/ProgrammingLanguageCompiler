import sys
from language_parser import LanguageParser
from language_lexer import LanguageLexer

source_file_name = sys.argv[1]
output_file_name = sys.argv[2]
source_file = open(source_file_name, 'r')
lexer = LanguageLexer()
parser = LanguageParser()
with open(source_file_name, 'r') as source_reader:
    source_code = source_reader.read()
    result = parser.parse(lexer.tokenize(source_code))