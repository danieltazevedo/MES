import random
from hypothesis import given,settings, Verbosity
from hypothesis import strategies as st
from parser import *
from generator import *

@settings(deadline=2000)
@given(number=st.integers(min_value=500, max_value=1000))
def test_pretty_printing(number):
    program = generate_program(number)
    for elem in program:
        parsing_output = parser_var.parse(elem)
        pretty_printing = recreate_code(parsing_output)
        pretty_printing_parsing = parser_var.parse(pretty_printing)
        assert parsing_output == pretty_printing_parsing

@settings(deadline=2000)
@given(number=st.integers(min_value=500, max_value=1000))
def test_smells_strategy(number):
    program = generate_program(number)
    for elem in program:      
        parsing_output = parser_var.parse(elem)

        p_td=smells_td(list(parsing_output))
        p_bu=smells_iner(list(parsing_output))
               
        assert p_td == p_bu
        
@settings(deadline=2000)
@given(number=st.integers(min_value=500, max_value=1000))
def test_otimizacoes_strategy(number):
    program = generate_program(number)
    for elem in program:      
        parsing_output = parser_var.parse(elem)

        p_td=otimizacoes_td(list(parsing_output))
        p_bu=otimizacoes_bu(list(parsing_output))
               
        assert p_td == p_bu

@settings(deadline=2000)
@given(number=st.integers(min_value=500, max_value=1000))
def test_smells_optimizations_comutative(number):
    program = generate_program(number)
    for elem in program:      
        parsing_output = parser_var.parse(elem)

        p_first_otimizacoes=otimizacoes_td(list(parsing_output))
        p_first_otimizacoes=smells_td(list(p_first_otimizacoes))

        p_first_smells=smells_td(list(parsing_output))
        p_first_smells=otimizacoes_td(list(p_first_smells))
               
        assert p_first_otimizacoes == p_first_smells
