import ply.yacc as yacc
from lexer import tokens
import zipper as zp
import strategy as stra
import random
from hypothesis import given
from hypothesis import strategies as st


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

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

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ('boolean',p[1])

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
    p[0] = p[0] + (p[3],)
    p[0] = p[0] + ('else',)
    p[0] = p[0] + (p[5],)

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
    p[0] = p[0] + ('while',)
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
    ' expression : IDENTIFIER LPAREN RPAREN'
    p[0] = ('call', p[1])

def p_expression_call_enpty(p):
    ' expression : IDENTIFIER LPAREN IDENTIFIER RPAREN'
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

parser_var = yacc.yacc()



def make_optimizations_td_bu(lst):
    if "binop" == lst[0]:
        r=lst
        if(lst[1] == "*"):
            if ("0") == lst[2][1] or ("0") in lst[3][1]:
                return ('number', '0')
            if ("1") == lst[2][1]:
                return otimizacoes_td(lst[3])
            if ("1") == lst[3][1]:
                return otimizacoes_td(lst[2]) 
       
            if "binop" == lst[2][0]:  
                o=list((lst[2][0],lst[2][1],lst[2][2],lst[2][3]))
                opt=otimizacoes_td(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_td(list((lst[0],lst[1],opt,lst[3]))))
            
            if "binop" == lst[3][0]:  
                o=list((lst[3][0],lst[3][1],lst[3][2],lst[3][3]))
                opt=otimizacoes_td(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_td(list((lst[0],lst[1],lst[2],opt))))

        if(lst[1] == "/"):
            if ("1") == lst[3][1]:
                return otimizacoes_td(lst[2])

        if(lst[1] == "+"):
            if ("0") == lst[2][1]:
                return otimizacoes_td(lst[3])
            if ("0") == lst[3][1]:
                return otimizacoes_td(lst[2])    
             
            if "binop" == lst[2][0]:  
                o=list((lst[2][0],lst[2][1],lst[2][2],lst[2][3]))
                opt=otimizacoes_td(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_td(list((lst[0],lst[1],opt,lst[3])))) 

            if "binop" == lst[3][0]:  
                o=list((lst[3][0],lst[3][1],lst[3][2],lst[3][3]))
                opt=otimizacoes_td(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_td(list((lst[0],lst[1],lst[2],opt))))
        return r
    else:
        return lst

def make_optimizations_iner(lst):
    if "binop" == lst[0]:
        r=lst
        if(lst[1] == "*"):
            if ("0") == lst[2][1] or ("0") in lst[3][1]:
                return ('number', '0')
            if ("1") == lst[2][1]:
                return otimizacoes_bu(lst[3])
            if ("1") == lst[3][1]:
                return otimizacoes_bu(lst[2]) 
       
            if "binop" == lst[2][0]:  
                o=list((lst[2][0],lst[2][1],lst[2][2],lst[2][3]))
                opt=otimizacoes_bu(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_bu(list((lst[0],lst[1],opt,lst[3]))))
            
            if "binop" == lst[3][0]:  
                o=list((lst[3][0],lst[3][1],lst[3][2],lst[3][3]))
                opt=otimizacoes_bu(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_bu(list((lst[0],lst[1],lst[2],opt))))

        if(lst[1] == "/"):
            if ("1") == lst[3][1]:
                return otimizacoes_bu(lst[2])

        if(lst[1] == "+"):
            if ("0") == lst[2][1]:
                return otimizacoes_bu(lst[3])
            if ("0") == lst[3][1]:
                return otimizacoes_bu(lst[2])    
             
            if "binop" == lst[2][0]:  
                o=list((lst[2][0],lst[2][1],lst[2][2],lst[2][3]))
                opt=otimizacoes_bu(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_bu(list((lst[0],lst[1],opt,lst[3])))) 

            if "binop" == lst[3][0]:  
                o=list((lst[3][0],lst[3][1],lst[3][2],lst[3][3]))
                opt=otimizacoes_bu(o)  
                if(opt!=o):
                    r=tuple(otimizacoes_bu(list((lst[0],lst[1],lst[2],opt))))
        if r == lst:  # Verifica se nenhuma otimização foi aplicada
            raise ValueError("Falha ao otimizar o nó")
        else:
            return r
    else:
        raise ValueError("Falha ao otimizar o nó")
    
def treat_smells(lst):
    if "binop" == lst[0]:
        if(lst[1] == "==" or lst[1] == "!="):
            if((lst[2][0] == "boolean" and lst[3][0] == "var") or (lst[2][0] == "boolean" and lst[3][0] == "call") ): 
                print("smells detected")
                return (lst[3][0], lst[3][1])
            if((lst[3][0] == "boolean" and lst[2][0] == "var") or (lst[3][0] == "boolean" and lst[2][0] == "call")):
                print("smells detected")
                return (lst[2][0], lst[2][1])
    if "function" == lst[0]:
        if(len(lst)>15):
            print("smells detected: big function")
    return lst

def treat_smells_iner(lst):
    if "binop" == lst[0]:
        if(lst[1] == "==" or lst[1] == "!="):
            if((lst[2][0] == "boolean" and lst[3][0] == "var") or (lst[2][0] == "boolean" and lst[3][0] == "call") ): 
                print("smells detected")
                return (lst[3][0], lst[3][1])
            if((lst[3][0] == "boolean" and lst[2][0] == "var") or (lst[3][0] == "boolean" and lst[2][0] == "call")):
                print("smells detected")
                return (lst[2][0], lst[2][1])
    if "function" == lst[0]:
        if(len(lst)>15):
            print("smells detected: big function")
    raise ValueError("Não foram detetados smells")
    
def otimizacoes_td(lst):
    z = zp.obj(lst)
    return stra.full_tdTP(lambda x: stra.adhocTP(stra.idTP, make_optimizations_td_bu, x), z).node()

def otimizacoes_bu(lst):
    z = zp.obj(lst)
    return stra.full_buTP(lambda x: stra.adhocTP(stra.idTP, make_optimizations_td_bu, x), z).node()

def otimizacoes_iner(lst):
    z = zp.obj(lst)
    return stra.innermost(lambda x: stra.adhocTP(stra.failTP, make_optimizations_iner, x), z).node()



def smells_td(lst):
    z = zp.obj(lst)
    return stra.full_tdTP(lambda x: stra.adhocTP(stra.idTP, treat_smells, x), z).node()

def smells_bu(lst):
    z = zp.obj(lst)
    return stra.full_buTP(lambda x: stra.adhocTP(stra.idTP, treat_smells, x), z).node()

def smells_iner(lst):
    z = zp.obj(lst)
    return stra.innermost(lambda x: stra.adhocTP(stra.failTP, treat_smells_iner, x), z).node()

def recreate_code(ast):
    if(len(ast)>0):
        node_type = ast[0]
        if  'assign ' in node_type:
            if(len(ast)<3):
                return f'{node_type[len(node_type)-1]} = {recreate_code(ast[1])}'
            else:
                return f'{node_type[len(node_type)-1]} = {recreate_code(ast[1])} ; {recreate_code(ast[2:])}'
        elif node_type == 'binop':
            if(len(ast)<5):
                return f'{recreate_code(ast[2])} {ast[1]} {recreate_code(ast[3])}'
            else:
                return f'{recreate_code(ast[2])} {ast[1]} {recreate_code(ast[3])} ; {recreate_code(ast[4:])}'
        elif node_type == 'number':
            if(len(ast)<3):
                return str(ast[1])
            else:
                return f'{ast[1]} ; {recreate_code(ast[2:])}'
        elif node_type == 'boolean':
            if(len(ast)<3):
                return ast[1]
            else:
                return f'{ast[1]} ; {recreate_code(ast[2:])}'
        elif node_type == 'var':
            if(len(ast)<3):
                return ast[1]
            else:
                return f'{ast[1]} ; {recreate_code(ast[2:])}'
        elif node_type == 'statement_list': 
            statements = [recreate_code(child) for child in ast[1:]]
            return '{' + recreate_code(ast[1:]) + '}'
        elif node_type == 'if':
            condition = recreate_code(ast[1])
            statement = recreate_code(ast[2:])
            return f'if ({condition}) {statement}'
        elif node_type == 'if_else':
            condition = recreate_code(ast[1])
            index = ast.index("else")
            elem = ast[2:index]
            if_statement = recreate_code(list(elem[0]))
            elem2 = ast[index+1:]
            else_statement = recreate_code(list(elem2[0]))
            return f'if ({condition}) {if_statement} else {else_statement}'
        elif node_type == 'while':
            condition = recreate_code(ast[1])
            statement = recreate_code(ast[2:])
            return f'while ({condition}) {statement}'
        elif node_type == 'for': 
            init_statement = recreate_code(ast[1:3])
            condition = recreate_code(ast[4])
            post_statement = recreate_code(ast[5:7])
            statement = recreate_code(ast[7:])
            return f'for ({init_statement}; {condition}; {post_statement}) {statement}'
        elif node_type == 'function':
            name = ast[1]
            arg_name = ast[2]
            statement = recreate_code(ast[3:])
            return f'def {name}({arg_name}): {statement}'
        elif node_type == 'call': 
            name = ast[1]
            if(len(ast)>2):
                arg = ast[2]
                return f'{name}({arg})'
            else:
                return f'{name}()'
        elif node_type == 'return':
            statement = recreate_code(ast[1:])
            return f'return {statement}'
        elif node_type == 'expr':
            return recreate_code(ast[1][0:])
        else:
            return ''
    else:
            return ''

