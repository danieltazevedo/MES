import ply.lex as lex

# List of token names.
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LCHAV',
    'RCHAV',
    'COMMAPOINT',
    'EQUALS',
    'IDENTIFIER',
    'TRUE',
    'FALSE',
    'IF',
    'ELSE',
    'WHILE',
    'DEFINE',
    'RETURN',
    'FOR',
    'AND',
    'OR',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQ',
    'NE',
)

# Regular expression rules for tokens.
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCHAV = r'{'
t_RCHAV = r'}'
t_COMMAPOINT = r';'
t_EQUALS = r'='
t_AND = r'&&'
t_OR  = r'\|\|'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

def t_NUMBER(t):
    r'\d+\.*\d*'
    return t

def t_IDENTIFIER(t):
    r'(?!if|else|while|for|define|return|false|true\b)[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_FOR(t):
    r'for'
    return t

def t_DEFINE(t):
    r'define'
    return t

def t_RETURN(t):
    r'return'
    return t

# Ignored characters.
t_ignore = ' \t\n'

# Error handling rule.
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()