import random
from hypothesis import given,settings, Verbosity
from hypothesis import strategies as st
from parser import *

# Função para gerar um nome válido
def generate_valid_name():
    valid_name = ""
    valid_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=1))
    return valid_name


# Função para gerar uma declaração aleatória
def generate_declaration():
    declaration = ""
    statement_type = random.choice(['assign','list','if','if_else', 'while', 'for'])
    if statement_type == 'assign':
        declaration = generate_assign()
    elif statement_type == 'list':
        random_number = random.randint(2, 10)
        declaration = "{"
        for _ in range(random_number):
            declaration = declaration + generate_assign() + ";"
        declaration = declaration + "}"
    elif statement_type == 'if':
        statement = generate_declaration()
        cond = generate_cond()
        declaration = f"if({cond}) {statement}"
    elif statement_type == 'if_else':
        statement1 = generate_declaration()
        statement2 = generate_declaration()
        cond = generate_cond()
        declaration = f"if({cond}) {statement1} else {statement2}"
    elif statement_type == 'while':
        statement = generate_declaration()
        cond = generate_cond()
        declaration = f"while({cond}) {statement}"
    elif statement_type == 'for':
        statement = generate_declaration()
        cond = generate_cond()
        a1 = generate_assign()
        a2 = generate_assign()
        declaration = f"for({a1};{cond};{a2}) {statement}"
    else:
        pass
    return declaration

def generate_assign():
    name = generate_valid_name()
    expression = generate_expression()
    assingn = f"{name} = {expression}"
    return assingn

# Função para gerar uma expressão aleatória
def generate_expression():
    # Gera uma expressão simples para este exemplo
    with_operation = random.choice(['true', 'false'])
    if with_operation == 'true':
        operation = random.choice(['+', '-','/','*'])
        value1 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=1))
        value2 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=1))
        return value1 + operation + value2
    else:
        value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=1))
        return str(value)
    
def generate_cond():
    operation = random.choice(['<=', '<','>=','>','==','!='])
    value1 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=1))
    value2 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=1))
    return value1 + operation + value2

def generate_program(number):
    program = []
    for _ in range(number):
        declaration = generate_declaration()
        program.append(declaration)
    return program

@settings(deadline=1000)
@given(number=st.integers(min_value=500, max_value=1000))
def test_generate_program(number):
    program = generate_program(number)
    for elem in program:
        parsing_output = parser_var.parse(elem)
        pretty_printing = recreate_code(parsing_output)
        pretty_printing_parsing = parser_var.parse(pretty_printing)
        assert parsing_output == pretty_printing_parsing

