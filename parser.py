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
    p[0] = ('assign '+p[1], p[3])    

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
    p[0] = ()
    p[0] = p[0] + ('statement_list',)
    for i in range(len(p[2])):
        p[0]=p[0]+(p[2][i],)

def p_statement_comma(p):
    'statement : statement COMMAPOINT statement'
    p[0] = ()
    p[0] = p[0] +(p[1][0],)
    p[0] = p[0] +(p[1][1],)
    for i in range(len(p[3])):
        p[0]=p[0]+(p[3][i],)
    

def p_statement_comma2(p):
    'statement : statement COMMAPOINT'
    p[0] = (p[1][0],p[1][1])

def p_statement_if_else(p):
    'statement : IF expression statement ELSE statement'
    p[0] = ()
    p[0] = p[0] + ('if_else',)
    p[0] = p[0] + (p[2],)
    for i in range(len(p[3])):
        p[0]=p[0]+(p[3][i],)
    for i in range(len(p[5])):
        p[0]=p[0]+(p[5][i],)



def p_statement_if(p):
    'statement : IF expression statement'
    p[0] = ()
    p[0] = p[0] + ('if',)
    p[0] = p[0] + (p[2],)
    for i in range(len(p[3])):
        p[0]=p[0]+(p[3][i],)

def p_statemen_for(p):
    'statement : FOR LPAREN statement COMMAPOINT statement COMMAPOINT statement RPAREN statement'
    p[0] = ('for',p[3],p[5],p[7],p[9])
    p[0] = ()
    p[0] = p[0] + ('for',)
    for i in range(len(p[3])):
        p[0]=p[0]+(p[3][i],)
    for i in range(len(p[5])):
        p[0]=p[0]+(p[5][i],)
    for i in range(len(p[7])):
        p[0]=p[0]+(p[7][i],)
    for i in range(len(p[9])):
        p[0]=p[0]+(p[9][i],)

    
    
def p_statement_while(p):
    'statement : WHILE expression statement'
    p[0] = ()
    p[0] = p[0] + ('if',)
    p[0] = p[0] + (p[2],)
    for i in range(len(p[3])):
        p[0]=p[0]+(p[3][i],)

def p_statement_function(p):
    'statement : DEFINE IDENTIFIER LPAREN IDENTIFIER RPAREN statement'
    p[0] = ()
    p[0] = p[0] + ('function',)
    p[0] = p[0] + (p[2],)
    p[0] = p[0] + (p[4],)
    for i in range(len(p[6])):
        p[0]=p[0]+(p[6][i],)


def p_expression_call(p):
    'statement : IDENTIFIER LPAREN IDENTIFIER RPAREN'
    p[0] = ('call', p[1], p[3])


def p_expression_return(p):
    'statement : RETURN statement'
    p[0] = ()
    p[0] = p[0] + ('return',)
    for i in range(len(p[2])):
        p[0]=p[0]+(p[2][i],)
    

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        parser.errok()
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def altera(lst):
    if "binop" == lst[0]:
        r=lst
        if(lst[1] == "*"):
            if ("0") == lst[2][1] or ("0") in lst[3][1]:
                return ('number', '0')
            if ("1") == lst[2][1]:
                return otimizacoes(lst[3])
            if ("1") == lst[3][1]:
                return otimizacoes(lst[2]) 
            if "binop" == lst[3][0]:  
                o=list((lst[3][0],lst[3][1],lst[3][2],lst[3][3]))
                opt=otimizacoes(o)  
                if(opt!=o):
                    r=tuple(otimizacoes(list((lst[0],lst[1],lst[2],tuple(opt)))))
                    
        if(lst[1] == "+"):
            if ("0") == lst[2][1]:
                return otimizacoes(lst[3])
            if ("0") == lst[3][1]:
                return otimizacoes(lst[2])    
            if "binop" == lst[3][0]:  
                o=list((lst[3][0],lst[3][1],lst[3][2],lst[3][3]))
                opt=otimizacoes(o)  
                if(opt!=o):
                    r=tuple(otimizacoes(list(lst[0],lst[1],lst[2],tuple(opt))))           
        return r
    else:
        return lst
    
def otimizacoes(lst):
    z = zp.obj(lst)
    return st.full_tdTP(lambda x: st.adhocTP(st.idTP, altera, x), z).node()

while True:
    try:
        s = input('bc > ')
    except EOFError:
        break
    p=parser.parse(s)
    print(list(p))
    p=otimizacoes(list(p))
    print(p)
