# lexer.py
# Documento que contém a parte léxica do projeto

import ply.lex as lex

# Dados feitos da classe a partir do exercício aula:    2021.12.17 - PL
class PortugolLexer:

    # Por fazer tokens específicas
    tokens = (...)

    # Copiado do exemplo stor, ver porquê
    t_ignore = " \t\n"

    # Função inicializadora do objeto
    def __init__(self):
        self.lex = lex.lex(module=self)

    # Função com expressão regular capaz de ler comentários
    def t_comentario(self, t):
        r"\#.*"
        pass

    # Função com expressão regular capaz de ler o símbolo de atruibuição de valor
    def t_atribuir(self, t):
        r"<-"
        return t

    # Função com expressão regular capaz de ler estruturas ciclicas, de decisao e declaracao de variaveis
    # Criar um def t_algo(self, t) para for, outro para if, etc? (Versão mais hardcoded)
z    def t_estruturas(self, t):
        r"[a-z]+"
        return t

    # Função com expressão regular capaz de ler o valor dado a um variavel tipo char
    def t_valor_string(self, t):
        r'"[^"]*"'
        return t

    # Função com expressão regular capaz de ler o valor de uma variavel tipo int, float, etc
    def t_valor_num(self, t):
        r"[0-9]+(\.[0-9]+)?"
        return t

    # Função para controlo de erros
    def t_error(self, t):
        raise Exception(f"Unexpected token: {t.value[:10]}")

    def token(self):
        return self.lex.token()
