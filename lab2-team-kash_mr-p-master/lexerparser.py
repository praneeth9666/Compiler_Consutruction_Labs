import ply.lex as lex 

#'MODULE', 'EXPR', 'CALL', 'NAME', 'LOAD', do we need to use these as tokens as well? Otherwise what do we do?
tokens = ('PRINT', 'INT', 'PLUS', 'MINUS', 'LPAR', 'RPAR', 'EVAL' )

t_PRINT = r'print'
t_EVAL = r'eval'
t_PLUS = r'\+'
t_MINUS = r'\-'

t_LPAR = r'\('
t_RPAR = r'\)'

def t_INT(t):
    r’\d+’
    try:
        t.value = int(t.value)
    except ValueError:
        print("integer value too large", t.value)
        t.value = 0
    return t

t_ignore  = ’ \t’

def t_newline(t):
    r’\n+’
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character ’%s’" % t.value[0])
    t.lexer.skip(1)



lex.lex()