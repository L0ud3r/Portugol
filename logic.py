# logic.py
from logic_grammar import LogicGrammar
import argparse




def run_batch(filename):
    with open(filename, "r") as f:
        content = f.read()
        content = "fim".join(content.split("fim")[:-1]) + "fim" #para que tudo o que esteja depois do ultimo fim seja tirado de content (para não ser lido nem interpretado)
        lg = LogicGrammar()
        try:
            ans = lg.parse(content)
            if ans is not None: #remover para apenas interpretar o codigo! (funcionamento normal de um compilador)
                print(ans) #remover para apenas interpretar o codigo! (funcionamento normal de um compilador)
        except Exception as exception:
            print(exception)





opcao = 0
while opcao != 1 and 2:
    print("Selecione uma opcao")
    opcao = int(input("Interpretar codigo: 1; \nGerar C: 2;\n>> "))
    if opcao == 1:
        file_path = input("Nome do ficheiro:\n>> ")
        run_batch(file_path)
    elif opcao == 2:
        print("Never gonna give you up.")




