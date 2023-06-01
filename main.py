from parser import *
from generator import *
from Mutations import *
import subprocess

def parsing():
    while True:
        try:
            s = input('bc > ')
        except EOFError:
            break
        if(s=="quit"):
            break
        p=parser_var.parse(s)
        print(p)
        print(recreate_code(p))

def parsing_otimizaçoes_smells():
    while True:
        try:
            s = input('bc > ')
        except EOFError:
            break
        if(s=="quit"):
            break
        p=parser_var.parse(s)
        p=otimizacoes_td(list(p))
        p=smells_td(list(p))
        print(p)
        print(recreate_code(p))

def execute_tests():
    command = ['python3', '-m', 'pytest', 'test.py']
    subprocess.run(command, check=True)


def mutantes():
    while True:
        try:
            s = input('bc > ')
        except EOFError:
            break
        if(s=="quit"):
            break
        p=parser_var.parse(s)
        print(p)
        p=mutation(list(p))
        print(p)
        print(recreate_code(p))

def main():
    while True:
        print("1 - Realizar Parsing")
        print("2 - Realizar Parsing+Otimizações+Smells")
        print("3 - Realizar Testes")
        print("4 - Gerar Programas")
        print("5 - Aplicar Mutantes")
        opcao = input("Digite a opção desejada (1 a 5):\n")


        if opcao == "1":
            parsing()        
        elif opcao == "2":
            parsing_otimizaçoes_smells()
        elif opcao == "3":
            execute_tests()
        elif opcao == "4":
            n=input("Indique o número de programas que deseja que sejam criados:\n")
            programs=generate_program(int(n))
            for p in programs:
                print(p)
                print("\n")
        elif opcao == "5":
            mutantes()
        elif opcao == "quit":
            break
        else:
            print("Opção inválida. Por favor, escolha '1' ou '5'.")

if __name__ == "__main__":
    main()


