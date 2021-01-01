from sly import Lexer

class LanguageLexer(Lexer):

    line_count = 1
    tokens = { NUMBER, DECLARE, BEGIN,  READ, WRITE, ENDIF, IF, THEN, ELSE,  ENDWHILE, 
     WHILE,
     REPEAT, UNTIL, FOR, FROM, DOWNTO, DO, TO, ENDFOR, EQUAL, ASSIGN, LESSEQUAL, 
     LESSTHAN, GREATEREQUAL, GREATERTHAN, NOTEQUAL, ID, COMMA, PLUS, MINUS, MULTI, DIV, MOD,
     LEFT, RIGHT, COLON, SEMICOLON, END}


    # String containing ignored characters
    ignore = ' \t\r'

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

    ID = r'[_a-z]+'

    ignore_comment = r'\[[^\]]*\]'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        LanguageLexer.line_count += t.value.count('\n')

    def error(self, t):
        raise Exception("Line "+str(LanguageLexer.line_count)+": Bad character " + str(t.value[0]))