# logic.py
from logic_grammar import LogicGrammar
import argparse


def run_interactively():
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
        lg = LogicGrammar()
        try:
            ans = lg.parse(content)
            if ans is not None:
                print(ans)
        except Exception as exception:
            print(exception)


parser = argparse.ArgumentParser()
parser.add_argument("--file",
                    help="Executes interactively",
                    type=str)
args = parser.parse_args()

if args.file is not None:
    run_batch(args.file)
else:
    run_interactively()



