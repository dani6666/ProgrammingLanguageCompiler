from sly import Lexer

class LanguageLexer(Lexer):

    tokens = { NUMBER, DECLARE, BEGIN,  READ, WRITE, ENDIF, IF, THEN, ELSE,  ENDWHILE, 
     WHILE,
     REPEAT, UNTIL, FOR, FROM, DOWNTO, DO, TO, ENDFOR, EQUAL, ASSIGN, LESSEQUAL, 
     LESSTHAN, GREATEREQUAL, GREATERTHAN, NOTEQUAL, ID, COMMA, PLUS, MINUS, MULTI, DIV, MOD,
     LEFT, RIGHT, COLON, SEMICOLON, END}


    # String containing ignored characters
    ignore = ' \t\r\n'

    # Regular expression rules for tokens
    COMMA       = r','
    DECLARE     = r'DECLARE'
    BEGIN       = r'BEGIN'
    READ        = r'READ'
    WRITE       = r'WRITE'
    ENDIF       = r'ENDIF'
    IF          = r'IF'
    THEN        = r'THEN'
    ELSE        = r'ELSE'
    ENDWHILE    = r'ENDWHILE'
    WHILE       = r'WHILE'
    REPEAT      = r'REPEAT'
    UNTIL       = r'UNTIL'
    FOR         = r'FOR'
    FROM        = r'FROM'
    DOWNTO      = r'DOWNTO'
    DO          = r'DO'
    TO          = r'TO'
    ENDFOR      = r'ENDFOR'
    PLUS        = r'\+'
    MINUS       = r'-'
    MULTI       = r'\*'
    DIV         = r'/'
    MOD         = r'%'
    EQUAL       = r'='
    ASSIGN      = r':='
    LESSEQUAL   = r'<='
    LESSTHAN    = r'<'
    GREATEREQUAL= r'>='
    GREATERTHAN = r'>'
    NOTEQUAL    = r'!='
    LEFT        = r'\('
    RIGHT       = r'\)'
    COLON       = r':'
    SEMICOLON   = r';'
    END         = r'END'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ignore_comment = r'\[[^\]]*\]'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1