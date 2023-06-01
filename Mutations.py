import random
from parser import *
from generator import *
import zipper as zp
import strategy as stra


def m(lst):
    if "binop" == lst[0]:
        if(lst[1] == "+"):
            return (lst[0],'-',lst[2],lst[3])
        if(lst[1] == '=='):
            return (lst[0],'!=',lst[2],lst[3])
        if(lst[1] == '*'):
            return ('number', '10')
        if(lst[1] == '>'):
            return (lst[0],'>=',lst[2],lst[3])
        if(lst[1] == '<='):
            return (lst[0],'<',lst[2],lst[3])
        if(lst[1] == '-'):
            return (lst[0],lst[1],lst[3],lst[2])
        if(lst[1] == '!='):
            return (lst[0],'>',lst[2],lst[3])
        if(lst[1] == '/'):
            return (lst[0],lst[1],lst[3],lst[2])
    return lst

def mutation(lst):
    z = zp.obj(lst)
    return stra.full_tdTP(lambda x: stra.adhocTP(stra.idTP, m, x), z).node()
