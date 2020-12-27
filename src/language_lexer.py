from sly import Lexer

class LanguageLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, DECLARE, BEGIN, END, READ, WRITE, IF, THEN, ELSE, ENDIF, WHILE, DO,
     ENDWHILE, REPEAT, UNTIL, FOR, FROM, TO, ENDFOR, DOWNTO, EQUALS, ASSIGN, LESSEQUAL, 
     LESSTHAN, GREATEREQUAL, GREATERTHAN, NOTEQUAL, ID, COMMA, PLUS, MINUS, MULTI, DIV }


    # String containing ignored characters
    ignore = ' \t\n'

    # Regular expression rules for tokens
    COMMA       = r','
    DECLARE     = r'DECLARE'
    BEGIN       = r'BEGIN'
    END         = r'END'
    READ        = r'READ'
    WRITE       = r'WRITE'
    IF          = r'IF'
    THEN        = r'THEN'
    ELSE        = r'ELSE'
    ENDIF       = r'ENDIF'
    WHILE       = r'WHILE'
    DO          = r'DO'
    ENDWHILE    = r'ENDWHILE'
    REPEAT      = r'REPEAT'
    UNTIL       = r'UNTIL'
    FOR         = r'FOR'
    FROM        = r'FROM'
    TO          = r'TO'
    ENDFOR      = r'ENDFOR'
    DOWNTO      = r'DOWNTO'
    PLUS        = r'\+'
    MINUS       = r'-'
    MULTI       = r'\*'
    DIV         = r'/'
    EQUALS      = r'='
    ASSIGN      = r':='
    LESSEQUAL   = r'<='
    LESSTHAN    = r'<'
    GREATEREQUAL= r'>='
    GREATERTHAN = r'>'
    NOTEQUAL    = r'!='
    LEFT        = r'('
    RIGHT       = r')'
    COLON       = r':'
    SEMICOLON   = r';'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1