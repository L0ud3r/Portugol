# logic.py
from logic_grammar import LogicGrammar
import argparse


def run_interactively(): #TODO: fazer o mesmo do fim aqui dentro!
    lg = LogicGrammar()
    for e in iter(lambda: input(">> "), ""):
        try:
            ans = lg.parse(e)
            if ans is not None:
                print(f"<< {ans}", end="\n\n")
        except Exception as exception:
            print(exception)


def run_batch(filename):
    with open(filename, "r") as f:
        content = f.read()
        content = "fim".join(content.split("fim")[:-1]) + "fim" #para que tudo o que esteja depois do ultimo fim seja tirado de content (para não ser lido nem interpretado)
        lg = LogicGrammar()
        try:
            ans = lg.parse(content)
            #if ans is not None: #remover para apenas interpretar o codigo! (funcionamento normal de um compilador)
            #    print(ans) #remover para apenas interpretar o codigo! (funcionamento normal de um compilador)
        except Exception as exception:
            print(exception)


parser = argparse.ArgumentParser()
parser.add_argument("--file",
                    help="Executes interactively",
                    type=str)
args = parser.parse_args()

run_batch("exemplo.esi")

#if args.file is not None:
#   run_batch(args.file)
#else:
#    run_interactively()



