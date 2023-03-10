import ply.yacc as yacc
from lexer import tokens
import zipper as zp
import strategy as st

# Definir as regras da gramática
def p_gramatica(p):
    'gramatica : statement'
    p[0] = p[1]

def p_statement_assign(p):
    'statement : IDENTIFIER EQUALS expression'
    p[0] = ('assign', p[1], p[3])

    

def p_statement_expr(p):
    'statement : expression'
    p[0] = ('expr', p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression AND expression
                  | expression OR expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('var', p[1])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_statement_list(p):
    'statement : LCHAV statement RCHAV'
    p[0] = ('statement_list', p[2])

def p_statement_comma(p):
    'statement : statement COMMAPOINT statement'
    p[0] = (p[1],p[3])

def p_statement_comma2(p):
    'statement : statement COMMAPOINT'
    p[0] = p[1]

def p_statement_if_else(p):
    'statement : IF expression statement ELSE statement'
    p[0] = ('if_else', p[2], p[3], p[5])

def p_statement_if(p):
    'statement : IF expression statement'
    p[0] = ('if', p[2],p[3])

def p_statemen_for(p):
    'statement : FOR LPAREN statement COMMAPOINT statement COMMAPOINT statement RPAREN statement'
    p[0] = ('for',p[3],p[5],p[7],p[9])
    
def p_statement_while(p):
    'statement : WHILE expression statement'
    p[0] = ('while', p[2], p[3])

def p_statement_function(p):
    'statement : DEFINE IDENTIFIER LPAREN IDENTIFIER RPAREN statement'
    p[0] = ('function', p[2], p[4], p[6])


def p_expression_call(p):
    'statement : IDENTIFIER LPAREN IDENTIFIER RPAREN'
    p[0] = ('call', p[1], p[3])


def p_expression_return(p):
    'statement : RETURN expression'
    p[0] = ('return', p[2])

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        parser.errok()
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def alteraDois(lst):
    if lst == '0':
        return '12'
    else:
        return lst
    
def alteraListaS(lst):
    z = zp.obj(lst)
    return st.full_tdTP(lambda x: st.adhocTP(st.idTP, alteraDois, x), z).node()

def flatten_tuple(expression_tuple):
    flattened_list = []
    for element in expression_tuple:
        if isinstance(element, tuple):
            flattened_list.extend(flatten_tuple(element))
        else:
            flattened_list.append(element)
    return flattened_list

while True:
    try:
        s = input('bc > ')
    except EOFError:
        break
    p=parser.parse(s)
    p=flatten_tuple(p)
    print(p)
    p=alteraListaS(list(p))
    print(p)
