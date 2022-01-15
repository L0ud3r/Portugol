# logic.py
from logic_grammar import LogicGrammar
import argparse


# Procedimento para ler um ficheiro e consoante o que é lido, chamar o lg.parse.
# O parse recebe o content e o output, para ou interpretar o código ou gerar o C.
def run_from_file(filename, output):
    with open(filename, "r") as f:
        content = f.read()
        content = "fim".join(content.split("fim")[:-1]) + "fim" #para que tudo o que esteja depois do ultimo fim seja tirado de content (para não ser lido nem interpretado)
        lg = LogicGrammar()
        try:
            ans = lg.parse(content, output)
            if ans is not None: #remover para apenas interpretar o codigo! (funcionamento normal de um compilador)
                print(ans) #remover para apenas interpretar o codigo! (funcionamento normal de um compilador)
        except Exception as exception:
            print(exception)

# Menu
opcao = 0
while opcao != 1 and opcao != 2:
    print("Selecione uma opcao")
    opcao = int(input("1: Interpretar codigo\n2: Gerar C:\n>> "))
    if opcao == 1:
        file_path = input("Nome do ficheiro:\n>> ")
        run_from_file(file_path, "interpreter")
    elif opcao == 2:
        file_path = input("Nome do ficheiro:\n>> ")
        run_from_file(file_path, "writer")




