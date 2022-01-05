# logic_grammar.py
import ply.yacc as yacc
from lexer import PortugolLexer


# Ideias tiradas de Aulas 2021.11.22 - D, 2021.11.24 - D e 2021.12.17-PL
class PortugolGrammar:

    def __init__(self, p):
        self.lexer = PortugolLexer()
        self.lexer.build(p)
        self.symbol = self.lexer.token()

    # Fazer recursividades descendentes

    def p_error(self, p):
        if p:
            raise Exception(f"Parse Error: Token inesperada: {p.type[:10]}")
        else:
            raise Exception("Parse Erro: Expecting token")

    def p_if(self, p):
        """if : se condicao codigo ';' fim_se"""

        p[0] = {
        "op": "se",
        "args": [p[2]],
        "data": [p[3]],
        }

    def p_if_else(self, p):
        """else : se condicao codigo ';' senao codigo; fim_se"""

        p[0] = {
            "op": ["se", "senão"],
            "args": [p[2], p[6]],
            "data": [p[3], p[7]],
        }

    def p_if_elseif(self, p):
        """else if : se condicao codigo ';' senao se condicao codigo; fim_se"""

        p[0] = {
            "op": "if",
            "args": [p[2], p[6]],
            "data": [p[3], p[7]],
        }


