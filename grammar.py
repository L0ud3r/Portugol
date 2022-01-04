# logic_grammar.py
import ply.yacc as yacc
from lexer import PortugolLexer


# Ideias tiradas de Aulas 2021.11.22 - D, 2021.11.24 - D e 2021.12.17-PL
class PortugolGrammar:

    def __init__(self, codigo):
        self.lexer = PortugolLexer()
        self.lexer.build(codigo)
        self.symbol = self.lexer.token()

    # Fazer recursividades descendentes
