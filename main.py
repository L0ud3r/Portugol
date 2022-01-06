# Portugol
# Cabeçalho de apresentação !!

from grammar import PortugolGrammar

def run_interactively():
    pg = PortugolGrammar()
    for e in iter(lambda: input(">> "), ""):
        try:
            ans = pg.parse(e)
            if ans is not None:
                print(f"<< {ans}", end = "\n\n")
        except Exception as exception:
            print(exception)

run_interactively()

