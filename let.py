import zipper as zp
import strategy as st
from adt import adt, Case


@adt
class Let:
    LET: Case["[Item]", "Exp"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            let=lambda l, e: "let " + strList(l) + "in " + str(e) + "\n"
        )


def strList(l):
    result = ""
    for i in l:
        result += str(i)
    return result


@adt
class Item:
    NESTEDLET: Case[str, "Let"]
    DECL: Case[str, "Exp"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            nestedlet=lambda s, l: s + " = " + str(l) + str(r),
            decl=lambda s, e: s + " = " + str(e) + "\n",
        )


@adt
class Exp:
    ADD: Case["Exp", "Exp"]
    MUL: Case["Exp", "Exp"]
    VAR: Case[str]
    CONST: Case[int]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            add=lambda x, y: str(x) + " + " + str(y),
            mul=lambda x, y: str(x) + " * " + str(y),
            var=lambda x: x,
            const=lambda x: str(x)
        )





let = Let.LET([Item.DECL("a", Exp.ADD(Exp.VAR("b"), Exp.CONST(3))), Item.DECL("c", Exp.MUL(Exp.CONST(4), Exp.VAR("a"))), Item.DECL("b", Exp.CONST(23))], Exp.VAR("c"))