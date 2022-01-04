# logic_grammar.py
import ply.yacc as yacc

class PortugolGrammar:
    precedente = (
        ...
    )

    def p_error(self, p):
        if p:
            raise Exception(f"Parse Error: Unexpected token '{p.type}'")
        else:
            raise Exception("Parse Error: Expecting token")

