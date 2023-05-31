import random
from parser import *
from generator import *
import zipper as zp
import strategy as stra

#Substitui a adição por subtração
def m1(lst):
    if "binop" == lst[0]:
        if(lst[1] == "+"):
            return (lst[0],'-',lst[2],lst[3])
    return lst

def mutation1(lst):
    z = zp.obj(lst)
    return stra.full_tdTP(lambda x: stra.adhocTP(stra.idTP, m1, x), z).node()


while True:
    try:
        s = input('bc > ')
    except EOFError:
        break
    p=parser_var.parse(s)
    p=otimizacoes_td(list(p))
    print(p)
    p=mutation1(list(p))
    print(p)
    print(recreate_code(p))